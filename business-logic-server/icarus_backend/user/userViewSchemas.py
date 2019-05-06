from schema import And, Optional

register_user_schema = {
    "username": And(str),
    "password": And(str),
    "email": And(str),
    "first_name": And(str),
    "last_name": And(str)
}

update_user_info_schema = {
    Optional("username"): And(str),
    Optional("password"): And(str),
    Optional("email"): And(str),
    Optional("picture_url"): And(str),
    Optional("first_name"): And(str),
    Optional("last_name"): And(str)
}

change_password_schema = {
    "old_password": And(str),
    "new_password": And(str)
}
