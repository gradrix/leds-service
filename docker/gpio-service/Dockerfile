FROM python:3-slim-buster

# OS deps
RUN apt update -y && apt-get install -y g++

# set working dir
WORKDIR /app

# upgrade pip & install dependencies
#RUN pip install --no-cache-dir --upgrade pip
COPY ./gpio-service/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# copy all the files to the container
COPY ./gpio-service/* ./

# setting up arguments
ARG port=9000
ARG pid=18
ARG ledCount=100

# setting up env variables
ENV LED_PORT=$port
ENV LED_PID=$pid
ENV LED_COUNT=$ledCount

# define the port number the container should expose
EXPOSE $port

# run the command
CMD [ "python", "./ledservice.py" ]