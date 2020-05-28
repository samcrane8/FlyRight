import os
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from users.tokens import account_activation_token
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from icarus_backend.celery import app
import smtplib


@app.task
def send_verification_email(username, email, user_id, domain):
    print('SENDING VERIFICATION EMAIL TO ', email)
    # mail_subject = 'Activate your Icarus Account'
    # message = render_to_string('acc_active_email.html', {
    #     'user': username,
    #     'domain': domain,
    #     'uid': urlsafe_base64_encode(force_bytes(user_id)).decode(),
    #     'token': account_activation_token.make_token(username),
    # })
    # email = EmailMessage(
    #     mail_subject, message, os.environ.get('EMAIL_ADDRESS', 'DEV'), to=[email]
    # )
    # email.send()
    sender = 'no-reply-flyright@police.gatech.edu'
    receivers = ['michael.ransby@gmail.com']

    message = """From: GTPD Flyright <no-reply-flyright@police.gatech.edu>
    To: To Person <""" + receivers[0] + """>
    Subject: SMTP e-mail test

    This is a test e-mail message.
    """

    try:
        smtpObj = smtplib.SMTP('outbound.gatech.edu')
        smtpObj.sendmail(sender, receivers, message)
        print("Successfully sent email")
    except SMTPException:
        print("Error: unable to send email")


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
