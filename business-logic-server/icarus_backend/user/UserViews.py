from django.template.response import TemplateResponse
from django.shortcuts import redirect
from rest_framework.decorators import api_view
from django.http import HttpResponse
import json
from users.models import IcarusUser as User
from icarus_backend.pilot.PilotModel import Pilot
from users.tokens import account_activation_token
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from icarus_backend.user.tasks import send_verification_email, reset_password_email
from django.contrib.sites.shortcuts import get_current_site
from icarus_backend.utils import validate_body
from oauth2_provider.decorators import protected_resource
from .userViewSchemas import *
from icarus_backend.user.UserController import UserController


@api_view(['POST'])
@validate_body(register_user_schema)
def icarus_register_user(request):
    b = request.data
    # Scrape the information from the request body JSON into the method params
    domain = get_current_site(request).domain
    status, message = UserController.register_user(b['username'], b['email'], b['password'],
                                                   b['first_name'], b['last_name'], domain)
    # What does the UserController have to say about our request?
    response_data = {'message': message}
    response_json = json.dumps(response_data)
    # Tell them about it
    return HttpResponse(response_json, content_type="application/json", status=status)


@protected_resource()
@api_view(['GET'])
def icarus_get_current_user(request):
    response_dict = dict()  # Make the JSON root
    response_dict['user'] = request.user.as_dict()
    pilot = Pilot.objects.filter(user=request.user).first()
    if pilot:
        response_dict['pilot'] = pilot.as_dict()
    response_json = json.dumps(response_dict)
    return HttpResponse(response_json, content_type="application/json", status=200)


@protected_resource()
@api_view(['GET'])
def icarus_get_user(request):
    # Get the user
    id = request.query_params.get('id')
    # What does the UserController have to say?
    status, response_dict = UserController.get_user(id)
    response_json = json.dumps(response_dict)
    # Give the user
    return HttpResponse(response_json, content_type="application/json", status=status)


@protected_resource()
@api_view(['POST'])
@validate_body(update_user_info_schema)
def update_user_info(request):
    parsed_json = request.data
    # Pass along the request JSON to the UserController
    status, data = UserController.update(request.user.id, parsed_json)
    # Return it
    return HttpResponse(json.dumps(data), content_type="application/json", status=status)


@api_view(['GET'])
def icarus_is_logged_in(request):  # Checks to see if there's the correct tokens attached, return false if not.
    if request.user.is_active:
        response_json = json.dumps(True)
        return HttpResponse(response_json, content_type="application/json", status=200)
    else:
        response_json = json.dumps(False)
        return HttpResponse(response_json, content_type="application/json", status=200)


@api_view(['GET'])
def activate(request, uidb64, token): # Activate the user, they got the link from their verification email
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=int(uid))
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user.username, token):
        user.is_active = True
        user.save()
        # TODO Define this link in the .env
        return redirect('https://flyright.police.gatech.edu/login')
        # return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')


@api_view(['GET'])
def forgot_password(request): # Find the user by email address, send them the appropriate link if the user exists.
    email = request.query_params.get('email')
    user = User.objects.filter(email=email).first()
    if user:
        domain = get_current_site(request).domain
        reset_password_email.delay(user.username, user.email, user.id, domain)
    response_data = {'message': 'If your account exists, a password reset email will be sent.'}
    response_json = json.dumps(response_data)
    return HttpResponse(response_json, content_type="application/json")


@api_view(['GET', 'POST'])
def reset_password_token(request, uidb64, token): # TODO Understand how this works
    if request.method == 'GET':
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=int(uid))
            validlink = True
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
            validlink = False
        return TemplateResponse(request, 'password_reset_confirm.html', {
            'validlink': validlink,
            'uid': uidb64,
            'token': token
        })
    elif request.method == 'POST':
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=int(uid))
            validlink = True
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
            validlink = False
        if user is not None and account_activation_token.check_token(user.username, token):
            body = request.data
            new_password = body['new_password']
            user.set_password(new_password)
            user.save()
            # return redirect('home')
            return HttpResponse('Your password has been updated. Now you can login your account.')
        else:
            return HttpResponse('Activation link is invalid!')


@protected_resource()
@api_view(['POST'])
@validate_body(change_password_schema)
def change_password(request): # Change the password of the user
    b = request.data
    status, message = UserController.change_password(request.user.email, b['old_password'],
                                                     b['new_password'])
    response_data = {'message': message}
    response_json = json.dumps(response_data)
    return HttpResponse(response_json, content_type="application/json", status=status)
