FROM python:3-slim-buster

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# OS deps
RUN apt update -y && apt-get install -y g++ gcc
RUN pip install --default-timeout=1000 --upgrade pip

# set working dir
WORKDIR /app

# install Python dependencies
COPY ./gpio-service/requirements.txt ./
RUN pip install --default-timeout=1000 --no-cache-dir -r requirements.txt

# copy all the files to the container
COPY ./gpio-service/ ./

# setting up arguments
ARG port=9000
ARG pin=18
ARG ledCount=100

# setting up env variables
ENV LED_PORT=$port
ENV LED_PIN=$pin
ENV LED_COUNT=$ledCount

# set working dir
WORKDIR /app

# copy all the files to the container
COPY ./gpio-service /app

# install Python dependencies
RUN pip install --default-timeout=1000 --no-cache-dir -r requirements.txt

# define the port number the container should expose
EXPOSE $port

# run the command
CMD [ "python", "main.py" ]
