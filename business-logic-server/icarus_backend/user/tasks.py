import os
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from users.tokens import account_activation_token
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from icarus_backend.celery import app
import smtplib


@app.task
#                                                   # TODO should domain be removed here?
def send_verification_email(user_first_name, email, user_id, domain):
    print('SENDING VERIFICATION EMAIL TO ', email)
    # TODO Move to .env, is this okay being passed as an arg?
    # domain = 'https://flyright-api.police.gatech.edu'
    uidb64 = urlsafe_base64_encode(force_bytes(user_id))
    token = account_activation_token.make_token(username)
    # TODO Remove my email. Make an env variable setting to send 'cc's to the admin.
    receivers = [email, 'michael.ransby+flyright@gmail.com']

    link = domain + """/user/activate/""" + uidb64 + """/""" + token
    sender = 'no-reply-flyright@police.gatech.edu'

    message = """From: GTPD Flyright <no-reply-flyright@police.gatech.edu>
To: """ + user_first_name + """ <""" + receivers[0] + """>
Content-type: text/html
Subject: GTPD Flyright Email Verification

G'day, """ + username + """<br><br>

Please click the link below to activate your GTPD Flyright account.<br><br>

<a href=""" + link + """>Click here to validate</a><br><br>

Kind Regards,<br>
Flyright Team.<br>
(Sent from tasks.py)
        """

    try:
        smtpObj = smtplib.SMTP('outbound.mail.gatech.edu')
        smtpObj.sendmail(sender, receivers, message)
        print("Successfully sent email")
    except:
        print("Error: unable to send email")

# TODO How does this work?
@app.task
def reset_password_email(username, email, user_id, domain):
    receivers = [email, 'michael.ransby@gmail.com']

    link = domain + """/reset_password/""" + uidb64 + """/""" + token
    sender = 'no-reply-flyright@police.gatech.edu'

    message = """From: GTPD Flyright <no-reply-flyright@police.gatech.edu>
    To: """ + username + """ <""" + receivers[0] + """>
    Content-type: text/html
    Subject: GTPD Flyright Reset Password

    G'day, """ + username + """<br><br>

    To initiate the password reset process for your Flyright Account,
click the link below:<br><br>

    <a href=""" + link + """>Click here to reset your password</a><br><br>

    Kind Regards,<br>
    Flyright Team.<br>
    (Sent from tasks.py)
            """
