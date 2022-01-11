#!/bin/bash

export DEBUG=1
export SECRET_KEY="1234567890"
export DJANGO_ALLOWED_HOSTS="*"
export GPIO_SERVICE_HOST=""
export LEDS_INSTALL_CFG="pin=18,port=9001,ledCount=100:pin=20,port=9002,ledCount=100"

cd ./web

until python3 manage.py migrate
do
    echo "Waiting for db to be ready..."
    sleep 2
done

python3 manage.py collectstatic --noinput

python3 manage.py runserver 0:8080
