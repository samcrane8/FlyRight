from .SchedulingRuleData import SchedulingRuleData
from .SchedulingRuleDTO import SchedulingRuleDTO
from .SchedulingRuleModel import SchedulingRule
from users.models import IcarusUser as User
from icarus_backend.flight.FlightModel import Flight
from .tasks import check_scheduling_rules
import json

class SchedulingRuleController:

    @staticmethod
    def register(scheduling_rule_data: SchedulingRuleData, flight_id: int) -> (int, dict):
        flight = Flight.objects.filter(id=flight_id).first()
        if not flight:
            return 400, {'message': 'Bad Flight ID.'}
        if scheduling_rule_data.ends_at == '':
            return 400, {'message': 'Not a valid datetime.'}
        scheduling_rule = SchedulingRuleDTO.data_to_db(scheduling_rule_data)
        scheduling_rule.save()
        flight.scheduling_rule = scheduling_rule
        flight.save()
        return 200, {'message': 'Scheduling rule successfully saved.'}

    @staticmethod
    def get(flight_id: int) -> (int, dict):
        flight = Flight.objects.filter(id=flight_id).first()
        if not flight:
            return 400, {'message': 'Bad Flight ID.'}
        if not flight.scheduling_rule:
            return 400, {'message': 'No scheduling rule for this flight.'}
        response_dict = flight.scheduling_rule.as_dict()
        return 200, response_dict

    @staticmethod
    def edit(new_scheduling_rule_data: SchedulingRuleData, flight_id: int) -> (int, dict):
        flight = Flight.objects.filter(id=flight_id).first()
        if not flight:
            return 400, {'message': 'Bad flight id.'}
        if not flight.scheduling_rule:
            return SchedulingRuleController.register(new_scheduling_rule_data, flight_id)
        scheduling_rule = flight.scheduling_rule
        scheduling_rule.frequency = new_scheduling_rule_data.frequency
        scheduling_rule.parameters = json.dumps(new_scheduling_rule_data.parameters)
        scheduling_rule.ends_at = new_scheduling_rule_data.ends_at
        scheduling_rule.save()
        return 200, {'message': 'Scheduling rule successfully updated.'}

    @staticmethod
    def delete(flight_id: int) -> (int, dict):
        flight = Flight.objects.filter(id=flight_id).first()
        if not flight:
            return 400, {'message': 'Bad Flight ID.'}
        if not flight.scheduling_rule:
            return 400, {'message': 'No scheduling rule exists for this flight.'}
        flight.scheduling_rule.delete()
        return 200, {'message': 'Scheduling rule successfully deleted.'}

    @staticmethod
    def get_user_rules(user_id: int) -> (int, dict):
        user = User.objects.filter(id=user_id).first()
        scheduling_rules = SchedulingRule.objects.filter(flight__created_by=user).all()
        response_dict = [rule.as_dict() for rule in scheduling_rules]
        return 200, response_dict

