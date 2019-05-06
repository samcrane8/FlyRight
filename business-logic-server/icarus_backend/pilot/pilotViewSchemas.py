from schema import And, Optional

register_pilot_schema = {
    "username": And(str),
    "password": And(str),
    "email": And(str),
    "remote_pilot_certificate_number": And(str),
    "mobile_phone_number": And(str),
    "first_name": And(str),
    "last_name": And(str)
}

update_pilot_info_schema = {
    Optional("remote_pilot_certificate_number"): And(str),
    Optional("mobile_phone_number"): And(str),
}