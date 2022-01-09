#!/bin/sh

until cd /app
do
    echo "Waiting for server volume..."
done

cd /app

until python manage.py migrate
do
    echo "Waiting for db to be ready..."
    sleep 2
done

python manage.py collectstatic --noinput

gunicorn django-main.wsgi:application --bind 0.0.0.0:8080 --workers 2 --threads 2