from .tasks import clearance_update_email
from .FlightData import FlightData
from .FlightDTO import FlightDTO
import uuid
from django.utils.timezone import is_aware
from django.contrib.gis.geos import Polygon

from icarus_backend.clearance.ClearanceModel import Clearance
from users.models import IcarusUser as User
from icarus_backend.drone.DroneModel import Drone
from .FlightModel import Flight
from icarus_backend.asset.AssetModel import Asset
from icarus_backend.department.DepartmentController import DepartmentController
from icarus_backend.department.DepartmentModel import Department
from notifications.signals import notify
from .tasks import new_flight_registered_email
from django.utils.dateparse import parse_datetime
from django.db.models import Q
from icarus_backend.utils import set_lat_range
from icarus_backend.settings import DEBUG


class FlightController:

    @staticmethod
    def register(flight_data: FlightData, user, domain) -> (int, dict):
        if not is_aware(flight_data.starts_at):
            return 400, {'message': 'Starts at has no timezone.'}
        if not is_aware(flight_data.ends_at):
            return 400, {'message':'Ends at has no timezone.'}
        flight_data.id = uuid.uuid4()
        clearance_id = uuid.uuid4()
        clearance = Clearance(clearance_id=clearance_id, created_by=user.username, state='PENDING',
                              message='')
        if len(flight_data.coordinates) < 4:
            return 403, {'message': 'Less than 3 coordinates given, this is not an area definition.'}
        new_flight = FlightDTO.data_to_db(flight_data, user, clearance)
        clearance.save()
        new_flight.save()
        departments = Department.objects.filter(area__intersects=new_flight.area).all()
        for department in departments:
            for airboss in department.airbosses.all():
                notify.send(user, recipient=airboss, verb='registered a flight', action_object=new_flight)
                if not DEBUG:
                    new_flight_registered_email.delay(airboss.username, airboss.email, airboss.id, domain)
            for watch_commanders in department.watchCommanders.all():
                notify.send(user, recipient=watch_commanders, verb='registered a flight', action_object=new_flight)
                if not DEBUG:
                    new_flight_registered_email.delay(watch_commanders.username, watch_commanders.email, watch_commanders.id, domain)
        return 200, {'id': str(flight_data.id)}

    @staticmethod
    def get_flights(user, method, body):
        user_owned_flights = Flight.objects
        department_flights = Flight.objects
        if method == 'POST':
            filters = body['filters']
            for _filter in filters:
                if _filter['title'] == 'before':
                    user_owned_flights = user_owned_flights.filter(ends_at__lt=parse_datetime(_filter['datetime']))
                    department_flights = department_flights.filter(ends_at__lt=parse_datetime(_filter['datetime']))
                if _filter['title'] == 'after':
                    user_owned_flights = user_owned_flights.filter(starts_at__gt=parse_datetime(_filter['datetime']))
                    department_flights = department_flights.filter(starts_at__gt=parse_datetime(_filter['datetime']))
        user_departments = DepartmentController.get_user_department_query(user)
        for user_department in user_departments:
            user_owned_flights = user_owned_flights.filter(~Q(area__intersects=user_department.area))
            department_flights = department_flights.filter(area__intersects=user_department.area)
        if len(user_departments) == 0:
            department_flights = []
        else:
            department_flights = department_flights.all()
        user_owned_flights = user_owned_flights.filter(created_by=user.id).all()
        dictionaries = []
        for flights, can_edit_clearance in [(department_flights, True), (user_owned_flights, False)]:
            for flight in flights:
                flight_dict = flight.as_dict()
                flight_dict['num_drones'] = Asset.objects.filter(flight=flight).count()
                flight_dict['can_edit_clearance'] = can_edit_clearance
                dictionaries += [flight_dict]
        return dictionaries

    @staticmethod
    def get_flight_info(flight_id, user) -> (int, dict):
        flight = Flight.objects.filter(id=flight_id).first()
        if not flight:
            return 400, {"message": "No mission exists with that id."}
        flight_dict = flight.as_dict()
        user_departments = DepartmentController.get_user_department_query(user)
        flight_dict['can_edit_clearance'] = False
        for user_department in user_departments:
            if flight.area.intersects(user_department.area):
                flight_dict['can_edit_clearance'] = True
        return 200, flight_dict

    @staticmethod
    def edit(flight_data: FlightData) -> (int, dict):
        flight = Flight.objects.filter(pk=flight_data.id).first()
        if flight_data.title:
            flight.title = flight_data.title
        if flight_data.description:
            flight.description = flight_data.description
        if flight_data.coordinates:
            coordinates = flight_data.coordinates['features'][0]['geometry']['coordinates']
            if coordinates[0][0] != coordinates[-1][0] or coordinates[0][1] != coordinates[-1][1]:
                coordinates += [coordinates[0]]
            area = []
            for coordinate in coordinates:
                area += [[coordinate[0], set_lat_range(coordinate[1])]]
            area = Polygon(area)
            flight.area = area
        if flight_data.starts_at:
            flight.starts_at = flight_data.starts_at
        if flight_data.ends_at:
            flight.ends_at = flight_data.ends_at
        if flight_data.type:
            flight.type = flight_data.type
        flight.save()
        return 200, {'message': flight.id}

    @staticmethod
    def add_drone(drone_id, mission_id, operator_id)->(int, dict):
        drone = Drone.objects.filter(id=drone_id).first()
        flight = Flight.objects.filter(id=mission_id).first()
        operator = User.objects.filter(id=operator_id).first()
        check_asset = Asset.objects.filter(flight=flight, drone=drone).first()
        if check_asset:
            return 400, {'message': 'Drone already added.'}
        asset = Asset(drone=drone, flight=flight, operator=operator)
        asset.save()
        return 200, {'message': 'Drone successfully added to mission.'}

    @staticmethod
    def remove_drone(drone_id, mission_id):
        drone = Drone.objects.filter(id=drone_id).first()
        flight = Flight.objects.filter(id=mission_id).first()
        asset = Asset.objects.filter(drone=drone, flight=flight).first()
        if not asset:
            return 400, {'message': 'Drone could not be removed because it was not attached to mission.'}
        asset.delete()
        return 200, {'message': 'Successfully removed drone from mission.'}

    @staticmethod
    def get_drones(flight_id):
        drones = Drone.objects.filter(asset__flight=flight_id).all()
        dictionaries = [obj.as_dict() for obj in drones]
        return 200, dictionaries

    @staticmethod
    def edit_clearance(user_id, flight_id, state, message) -> (int, dict):
        user = User.objects.filter(id=user_id).first()
        flight = Flight.objects.get(id=flight_id)
        if not DepartmentController.can_edit(user, flight):
            return 400, {'message': 'You do not have permissions to edit this flights clearance.'}
        object = flight.clearance
        object.created_by = user.username
        object.state = state
        object.message = message
        object.save()
        user = flight.created_by
        clearance_update_email.delay(user.username, user.email, user.username, flight.title, message, state)
        notify.send(user, recipient=flight.created_by, verb='updated flight clearance', action_object=flight)
        return 200, {'message': 'Successfully edited the clearance.'}

    @staticmethod
    def can_edit_clearance(flight):
        pass