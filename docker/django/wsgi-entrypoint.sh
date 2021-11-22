#!/bin/sh

until cd /app/backend
do
    echo "Waiting for server volume..."
done

cd /app/backend

until python manage.py migrate
do
    echo "Waiting for db to be ready..."
    sleep 2
done

python manage.py collectstatic --noinput

gunicorn django-main.wsgi --bind 0.0.0.0:8080 --workers 2 --threads 2

#####################################################################################
# Options to DEBUG Django server
# Optional commands to replace abouve gunicorn command

# Option 1:
# run gunicorn with debug log level
# gunicorn server.wsgi --bind 0.0.0.0:8080 --workers 1 --threads 1 --log-level debug

# Option 2:
# run development server
# DEBUG=True ./manage.py runserver 0.0.0.0:8080
