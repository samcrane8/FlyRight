from schema import And, Optional

# Define the schemas for request bodies in UserViews.py
# We must have all of the information for a new user
register_user_schema = {
    "username": And(str),
    "password": And(str),
    "email": And(str),
    "first_name": And(str),
    "last_name": And(str)
}

# We only want the items the user is updating here
update_user_info_schema = {
    Optional("username"): And(str),
    Optional("password"): And(str),
    Optional("email"): And(str),
    Optional("picture_url"): And(str),
    Optional("first_name"): And(str),
    Optional("last_name"): And(str)
}

# Make sure they know the old password and the new one
change_password_schema = {
    "old_password": And(str),
    "new_password": And(str)
}
