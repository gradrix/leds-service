#!/bin/bash

docker stop leds-flask-app >/dev/null 2>&1 && docker rm leds-flask-app >/dev/null 2>&1

docker build -t leds-flask-app -f docker/web_api/Dockerfile .

docker run -it -d --network host -v $(pwd)/frontend_build:/app/frontend_build --name leds-flask-app --restart unless-stopped leds-flask-app
#docker run -d -p 80:80 -v $(pwd)/frontend_build:/app/frontend_build --name leds-flask-app leds-flask-app