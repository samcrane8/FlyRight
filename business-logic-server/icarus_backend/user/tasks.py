import os
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from users.tokens import account_activation_token
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from icarus_backend.celery import app


@app.task
def send_verification_email(username, email, user_id, domain):
    mail_subject = 'Activate your Icarus Account'
    message = render_to_string('acc_active_email.html', {
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
def reset_password_email(username, email, user_id, domain):
    mail_subject = 'Reset Password'
    message = render_to_string('reset_password.html', {
        'user': username,
        'domain': domain,
        'uid': urlsafe_base64_encode(force_bytes(user_id)).decode(),
        'token': account_activation_token.make_token(username),
    })
    email = EmailMessage(
        mail_subject, message, secrets["email"]["from"], to=[email]
    )
    email.send()