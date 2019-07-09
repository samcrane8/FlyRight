import os
from icarus_backend.celery import app
from django.core.mail import EmailMessage
from django.template.loader import render_to_string


class DepartmentTasks:

    @staticmethod
    @app.task
    def email_jurisdiction(username, email, gov_official_username, clearance_message):
        mail_subject = '[Icarus] Message from Local Authority'
        message = render_to_string('jurisdiction_pilots_message.html', {
            'user': username,
            'message': clearance_message,
            'gov_off': gov_official_username,
        })
        email = EmailMessage(
            mail_subject, message, os.environ.get('EMAIL_ADDRESS', 'DEV'), to=[email]
        )
        email.send()

