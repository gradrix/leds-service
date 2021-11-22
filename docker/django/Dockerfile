FROM python:3

# set working dir
WORKDIR /app/backend

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# upgrade pip & install dependencies
RUN pip install --upgrade pip
COPY ./backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# copy all project files to the container
COPY ./docker/django/wsgi-entrypoint.sh ./
COPY ./backend ./
