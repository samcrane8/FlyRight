import requests
import json, os
import time
import math
from copy import copy
from django.conf import settings
from django.utils.log import AdminEmailHandler
from django.views.debug import ExceptionReporter


class SlackExceptionHandler(AdminEmailHandler):

    # replacing default django emit (https://github.com/django/django/blob/master/django/utils/log.py)
    def emit(self, record, *args, **kwargs):

        # original AdminEmailHandler "emit" method code (but without actually sending email)
        try:
            request = record.request
            subject = '%s (%s IP): %s' % (
                record.levelname,
                ('internal' if request.META.get('REMOTE_ADDR') in settings.INTERNAL_IPS
                 else 'EXTERNAL'),
                record.getMessage()
            )
        except Exception:
            subject = '%s: %s' % (
                record.levelname,
                record.getMessage()
            )
            request = None
        subject = self.format_subject(subject)

        # Since we add a nicely formatted traceback on our own, create a copy
        # of the log record without the exception data.
        no_exc_record = copy(record)
        no_exc_record.exc_info = None
        no_exc_record.exc_text = None

        if record.exc_info:
            exc_info = record.exc_info
        else:
            exc_info = (None, record.getMessage(), None)

        reporter = ExceptionReporter(request, is_email=True, *exc_info)
        message = "%s\n\n%s" % (self.format(no_exc_record), reporter.get_traceback_text())
        html_message = reporter.get_traceback_html() if self.include_html else None

        # self.send_mail(subject, message, fail_silently=True, html_message=html_message)

        # this is where original "emit" method code ends

        user_value = 'No Request'
        if hasattr(request, 'user'):
            if request.user.is_authenticated:
                user_value = request.user.username + ' (' + str(request.user.pk) + ')'
            else:
                user_value = 'Anonymous'

        # construct slack attachment detail fields
        attachments = [
            {
                'title': subject,
                'color': 'danger',
                'fields': [
                    {
                        "title": "Build",
                        "value": os.environ.get('FLYRIGHT_BUILD', 'DEV'),
                        "short": True,
                    },
                    {
                        "title": "Level",
                        "value": record.levelname,
                        "short": True,
                    },
                    {
                        "title": "Method",
                        "value": request.method if request else 'No Request',
                        "short": True,
                    },
                    {
                        "title": "Path",
                        "value": request.path if request else 'No Request',
                        "short": True,
                    },
                    {
                        "title": "User",
                        "value": user_value,
                        "short": True,
                    },
                    {
                        "title": "Status Code",
                        "value": (record.status_code if record.status_code else 'Undefined'),
                        "short": True,
                    },
                    {
                        "title": "UA",
                        "value": (request.META['HTTP_USER_AGENT']
                                  if request and request.META and 'HTTP_USER_AGENT' in request.META.keys() else 'No Request'),
                        "short": False,
                    },
                    {
                        "title": 'GET Params',
                        "value": json.dumps(request.GET) if request else 'No Request',
                        "short": False,
                    },
                    {
                        "title": "POST Data",
                        "value": json.dumps(request.POST) if request else 'No Request',
                        "short": False,
                    },
                ],
            },

        ]

        # add main error message body

        # slack message attachment text has max of 8000 bytes
        # lets split it up into 7900 bytes long chunks to be on the safe side

        split = 7900
        parts = range(math.ceil(len(message.encode('utf8')) / split))

        for part in parts:
            start = 0 if part == 0 else split * part
            end = split if part == 0 else split * part + split

            # combine final text and prepend it with line breaks
            # so the details in slack message will fully collapse
            detail_text = '\r\n\r\n\r\n\r\n\r\n\r\n\r\n' + message[start:end]

            attachments.append({
                'color': 'danger',
                'title': 'Details (Part {})'.format(part + 1),
                'text': detail_text,
                'ts': time.time(),
            })

        # construct main text
        main_text = 'Error at ' + time.strftime("%A, %d %b %Y %H:%M:%S +0000", time.gmtime())

        # construct data
        data = {
            'payload': json.dumps({'main_text': main_text, 'attachments': attachments}),
        }

        # send it
        if os.environ.get('SLACKBOT_ENABLED', 'disabled') == 'enabled':
            webhook_url = os.environ.get('SLACKBOT_WEBHOOK_URL', 'DEV')
            r = requests.post(webhook_url, data=data)