FROM python:3

# set a directory for the app
WORKDIR /usr/src/app

# install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy all the files to the container
COPY ./app .

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
