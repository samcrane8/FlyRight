from icarus_backend.celery import app
from icarus_backend.gateways.SlackBotGateway import post_health
from .SchedulingRuleModel import SchedulingRule
from .SchedulingRuleDTO import SchedulingRuleDTO
from icarus_backend.flight.FlightModel import Flight
from icarus_backend.flight.FlightData import FlightData
from icarus_backend.flight.FlightDTO import FlightDTO
from icarus_backend.flight.FlightController import FlightController
from django.utils import timezone
import datetime
import json
import pytz


@app.task
def check_scheduling_rules():
    _now = timezone.now()
    scheduling_rules = SchedulingRule.objects.filter(ends_at__gt=_now).all()
    for scheduling_rule in scheduling_rules:
        scheduling_rule_data = SchedulingRuleDTO.db_to_data(scheduling_rule)
        flight = Flight.objects.filter(scheduling_rule=scheduling_rule).latest('created_at')
        flight_data = FlightDTO.db_to_data(flight)

        start_time = flight.starts_at.time()
        duration = flight.ends_at - flight.starts_at
        today = datetime.date.today()

        for day in scheduling_rule_data.parameters['days']:

            day_int = day_to_int(day)
            start_date = today - datetime.timedelta(days=-today.weekday()-1+day_int, weeks=1)
            start_datetime = datetime.datetime.combine(start_date, start_time)
            start_datetime = timezone.make_aware(start_datetime, timezone=pytz.timezone('UTC'))
            end_datetime = start_datetime + duration
            flight_data.starts_at = start_datetime
            flight_data.ends_at = end_datetime
            conflicting_flight = Flight.objects.filter(area__intersects=flight.area,
                                                       starts_at__lte=start_datetime,
                                                       ends_at__gte=end_datetime).first()
            if conflicting_flight:
                continue
            status, response_dict = FlightController.register(flight_data,
                                                              flight.created_by,
                                                              None)
            flight_id = response_dict['id']
            _, drones = FlightController.get_drones(flight.id)
            for drone in drones:
                FlightController.add_drone(drone['id'], flight_id, flight.created_by.id)
            made_flight = Flight.objects.filter(id=flight_id).first()
            made_flight.scheduling_rule = scheduling_rule
            made_flight.save()


def day_to_int(day):
    if day == 'SU':
        return 0
    elif day == 'M':
        return 1
    elif day == 'T':
        return 2
    elif day == 'W':
        return 3
    elif day == 'TH':
        return 4
    elif day == 'F':
        return 5
    elif day == 'S':
        return 6
