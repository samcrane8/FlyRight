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
    domain = 'https://flyright-api.police.gatech.edu'
    uidb64 = urlsafe_base64_encode(force_bytes(user_id))
    token = account_activation_token.make_token(username)
    receivers = [email, 'michael.ransby@gmail.com']

    link = domain + """/user/activate/""" + uidb64 + """/""" + token
    sender = 'no-reply-flyright@police.gatech.edu'

    message = """From: GTPD Flyright <no-reply-flyright@police.gatech.edu>
To: """ + username + """ <""" + receivers[0] + """>
Content-type: text/html
Subject: GTPD Flyright Email Verification

G'day, """ + username + """<br><br>

Please click the link below to activate your GTPD Flyright account.<br><br>

<a href=""" + link+ """>Me!</a><br><br>

Kind Regards,<br>
Flyright Team.<br>
(Sent from tasks.py)
        """

    try:
        smtpObj = smtplib.SMTP('outbound.gatech.edu')
        smtpObj.sendmail(sender, receivers, message)
        print("Successfully sent email")
    except: 
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
