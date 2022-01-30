FROM python:3-slim-buster

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# OS deps
RUN apt update -y && apt-get install -y g++ gcc
RUN pip install --default-timeout=1000 --upgrade pip

# set working dir
WORKDIR /app

# upgrade pip & install dependencies
COPY ./web/requirements.txt ./
RUN pip install --default-timeout=1000 --no-cache-dir -r requirements.txt

# copy all project files to the container
COPY ./docker/django/wsgi-entrypoint.sh ./
COPY ./web/ ./
