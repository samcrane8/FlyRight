import json


class SchedulingRuleData:

    def __init__(self, frequency, parameters, ends_at):
        self.frequency = frequency
        self.parameters = parameters
        self.ends_at = ends_at

    @staticmethod
    def from_json(json_object):
        return SchedulingRuleData(json_object['frequency'],
                                  json_object['parameters'],
                                  json_object['ends_at'])
