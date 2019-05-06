from schema import And


class DepartmentSchemas:

    create = {
        "name": And(str),
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
        "owner_id": And(int),
    }

    edit = {
        "name": And(str),
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
        "new_name": And(str),
    }

    flight_histogram_schema = {
            "start_day": And(str),
            "end_day": And(str),
            "department_id": And(int)
        }

    email_jurisdiction_schema = {
        "message": And(str),
        "department_name": And(str)
    }