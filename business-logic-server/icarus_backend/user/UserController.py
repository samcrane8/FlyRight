from django.contrib.auth import authenticate
from users.tokens import account_activation_token
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from users.models import IcarusUser as User
from icarus_backend.pilot.PilotModel import Pilot
from icarus_backend.user.tasks import send_verification_email
from django.template.loader import render_to_string

import smtplib


class UserController:
    @staticmethod
    def register_user(username, email, password, first_name, last_name, domain) -> (int, str):
        # Find if there's already a user with this email
        user = User.objects.filter(email=email).first()
        if user is not None:
            # Return a 400 if there is, they should be using the reset password feature.
            return 400, 'Email address has already been taken.'
        # Do the same again with the username
        user = User.objects.filter(username=username).first()
        if user is None:
            # Creat the user
            user = User.objects.create_user(username=username,
                                            email=email,
                                            password=password,
                                            first_name=first_name,
                                            last_name=last_name,
                                            role='pilot')
            # Ensure the user isn't able to use their account yet, they must activate it through the verification email.
            user.is_active = False
            # Commit to DB
            user.save()
            # Send the verification email.
            send_verification_email.delay(user.first_name¡, user.email, user.id, domain)

            return 200, 'User successfully registered.'
        else:
            return 400, 'Username already taken.'

    @staticmethod
    def change_password(email, old_password, new_password) -> (int, str):
        # Find the user
        user = User.objects.filter(email=email).first()
        # Check their old password is correct
        if not user.check_password(old_password):
            return 400, 'Incorrect old password.'
        # Set the new one
        user.set_password(new_password)
        # Commit to DB
        user.save()
        return 200, 'Password successfully changed.'

    @staticmethod
    def get_user(id) -> (int, dict):
        # Find the user
        user = User.objects.filter(id=id).first()
        # No user found, return a 400
        if not user:
            return 400, {'message': 'No user with this id exists.'}
        # Make the JSON response, we found a user
        response_dict = dict()  # Root object
        response_dict['user'] = user.as_dict()
        pilot = Pilot.objects.filter(user=user).first()
        if pilot:
            response_dict['pilot'] = pilot.as_dict() # Also provide the information about this user as a pilot
        return 200, response_dict # Give them the information

    @staticmethod
    def update(id, parsed_json):
        # TODO is there a better way of doing this?
        user = User.objects.filter(id=id).first() # Find the user by pk
        # Update any of the fields, if they have been provided in the request.
        if 'email' in parsed_json and user.email != parsed_json['email']:
            user.email = parsed_json['email']
        if 'password' in parsed_json and user.password != parsed_json['password']:
            user.password = parsed_json['password']
        if 'username' in parsed_json and user.username != parsed_json['username']:
            check_user = User.objects.filter(username=parsed_json['username']).first()
            if check_user:
                return 401, {'message': 'Username already taken.'}
            user.username = parsed_json['username']
        if 'first_name' in parsed_json and user.first_name != parsed_json['first_name']:
            user.first_name = parsed_json['first_name']
        if 'last_name' in parsed_json and user.last_name != parsed_json['last_name']:
            user.last_name = parsed_json['last_name']
        if 'picture_url' in parsed_json and user.picture_url != parsed_json['picture_url']:
            user.picture_url = parsed_json['picture_url']
        # Commit to DB
        user.save()
        return 200, {'message': 'Info updated successfully.'}
