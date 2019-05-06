from schema import And, Optional


class FlightViewSchemas:

    get_flights_schema = {
        "filters": And(list),
    }

    edit_flight_schema = {
        "mission_id": And(str),
        Optional("area"): And(dict),
        Optional("description"): And(str),
        Optional("title"): And(str),
        Optional("starts_at"): And(str),
        Optional("ends_at"): And(str),
        Optional("type"): And(str)
    }

    add_drone_to_flight_schema = {
        "mission_id": And(str),
        "drone_id": And(str),
        "operator_id": And(str),
    }

    remove_drone_from_flight_schema = {
        "mission_id": And(str),
        "drone_id": And(str),
    }

    get_flight_info_schema = {
        "mission_id": And(str)
    }