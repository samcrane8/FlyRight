# icarus-app-server
This is the Application Server of the Icarus Drone management system.


## Setup

For setting up, use the appropriate bash script for installation.

For example, for Ubuntu 16.04, use the `install_on_ubuntu_16_04.sh` file.

If you have a different operating system you may need to apply some modifications to
get your system working. New scripts to handle different OS's would be greatly appreciated.

## Run

First, make sure you are in the virtual environment: `source venv/bin/activate`

### Single-Line

There is a single line script that runs each of these commands. It is slightly more convenient
than doing manually. 

Just simply write: `sh run_server_on_{CURRENT_OS}.sh` for whichever OS you are running on.

### Manually

You will need four different `screen` instances with the following commands typed in to run this server: 

First one is the django server: `python manage.py runserver`

Or to run through gunicorn: `gunicorn --bind 0.0.0.0:8000 icarus_backend.wsgi:application`

Second one is the redis-server: `redis-server`

Third one is the celery worker: `celery worker -A icarus_backend --loglevel=debug --concurrency=1`

Fourth one is the celery beat: `celery beat -A icarus_backend --loglevel=debug --scheduler django_celery_beat.schedulers:DatabaseScheduler`

### Nginx Proxy

There 

## Authentication

We use OAuth2 to authenticate users, though for superusers we also have the model backend. 