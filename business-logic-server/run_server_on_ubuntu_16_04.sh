#!/usr/bin/env bash
screen -S http-server gunicorn --bind 0.0.0.0:8000 icarus_backend.wsgi:application
screen -S redis-server redis-server
screen -S celery-worker celery worker -A icarus_backend --loglevel=debug --concurrency=1
screen -S celery-beat celery beat -A icarus_backend --loglevel=debug --scheduler django_celery_beat.schedulers:DatabaseScheduler