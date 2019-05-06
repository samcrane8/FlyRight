import json

from .SchedulingRuleData import SchedulingRuleData
from .SchedulingRuleModel import SchedulingRule
from icarus_backend.flight.FlightModel import Flight


class SchedulingRuleDTO:

    @staticmethod
    def data_to_db(scheduling_rule_data: SchedulingRuleData) -> SchedulingRule:
        return SchedulingRule(frequency=scheduling_rule_data.frequency,
                              parameters=json.dumps(scheduling_rule_data.parameters),
                              ends_at=scheduling_rule_data.ends_at)

    @staticmethod
    def db_to_data(scheduling_rule: SchedulingRule):
        return SchedulingRuleData(frequency=scheduling_rule.frequency,
                                  parameters=json.loads(scheduling_rule.parameters),
                                  ends_at=str(scheduling_rule.ends_at))
