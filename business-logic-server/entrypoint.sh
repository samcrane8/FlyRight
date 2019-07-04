#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."
    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

ls

python3 ../business-logic-server/manage.py makemigrations osiris_server
python3 ../business-logic-server/manage.py migrate
echo "MIGRATED"

exec "$@"
