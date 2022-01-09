#!/bin/bash

export DEBUG=1
export SECRET_KEY="1234567890"
export DJANGO_ALLOWED_HOSTS="localhost 127.0.0.1 [::1] leds leds.lan"
export GPIO_SERVICE_HOST=""

cd ./web

until python3 manage.py migrate
do
    echo "Waiting for db to be ready..."
    sleep 2
done

python3 manage.py collectstatic --noinput

python3 manage.py runserver 0:8080
