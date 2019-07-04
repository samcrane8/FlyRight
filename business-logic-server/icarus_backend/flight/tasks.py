import os
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from users.tokens import account_activation_token
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from icarus_backend.celery import app


@app.task
def new_flight_registered_email(username, email, user_id, domain):
    mail_subject = '[Icarus] New Flight Registered'
    message = render_to_string('new_mission_registered.html', {
        'user': username,
        'domain': domain,
        'uid': urlsafe_base64_encode(force_bytes(user_id)).decode(),
        'token': account_activation_token.make_token(username),
    })
    email = EmailMessage(
        mail_subject, message, os.environ.get('EMAIL_ADDRESS', 'DEV'), to=[email]
    )
    email.send()


@app.task
def clearance_update_email(username, email, gov_official_username, flight_title, clearance_message, state):
    mail_subject = '[Icarus] Flight Clearance Updated'
    message = render_to_string('flight_clearance_update.html', {
        'user': username,
        'flight_title': flight_title,
        'message': clearance_message,
        'gov_off': gov_official_username,
        'state': state,
    })
    email = EmailMessage(
        mail_subject, message, secrets["email"]["from"], to=[email]
    )
    email.send()
