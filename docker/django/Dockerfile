FROM python:3-slim-buster

# OS deps
RUN apt update -y && apt-get install -y g++

# set working dir
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# upgrade pip & install dependencies
#RUN pip install --no-cache-dir --upgrade pip
COPY ./web/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# copy all project files to the container
COPY ./docker/django/wsgi-entrypoint.sh ./
COPY ./web/manage.py ./
COPY ./web/api ./api
COPY ./web/django-main ./django-main
