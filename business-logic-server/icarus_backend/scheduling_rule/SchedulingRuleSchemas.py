from schema import And, Optional


class SchedulingRuleSchemas:

    register = {
        "flight_id": And(str),
        "frequency": And(str),
        "parameters": And(dict),
        "ends_at": And(str)
    }

    edit = {
        "flight_id": And(str),
        "frequency": And(str),
        "parameters": And(dict),
        "ends_at": And(str)
    }

    delete = {
        "flight_id": And(str)
    }