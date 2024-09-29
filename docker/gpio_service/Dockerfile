FROM python:3-slim-buster

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# OS deps
RUN apt update -y && apt-get install -y g++ gcc

# Copy the requirements file to the container
COPY ./gpio_service/requirements.txt .

# install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# setting up arguments
ARG port=9001
ARG pin=18
ARG ledCount=360

# setting up env variables
ENV LED_PORT=$port
ENV LED_PIN=$pin
ENV LED_COUNT=$ledCount

# set working dir
WORKDIR /app

# copy all the files to the container
COPY ./gpio_api ./gpio_api
COPY ./gpio_service ./gpio_service

# define the port number the container should expose
EXPOSE $port

# run the command
CMD [ "python", "-m", "gpio_service.main" ]
