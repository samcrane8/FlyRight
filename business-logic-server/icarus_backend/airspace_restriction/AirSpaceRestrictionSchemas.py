from schema import And, Optional

add_airspace_restriction_schema = {
    "is_constant": And(bool),
    "starts_at": And(str),
    "ends_at": And(str),
    "area": {
        "type": And(str),
        "features": [{
            "properties": And(dict),
            "type": And(str),
            "geometry": {
                "type": And(str),
                "coordinates": And(list)
            }
        }]
    },
    "type": And(str),
    "title": And(str),
    "description": And(str)
}