#!/bin/bash
# export LED_COUNT=360
# export LED_PORT=$2
# export LED_PIN=$1

# sudo -E python3 ./gpio_service/main.py

docker build -t leds-service --build-arg pin=18 --build-arg port=9001 --build-arg ledCount=360 -f ./docker/gpio_service/Dockerfile .

docker run --name leds-service -it -d --device /dev/gpiomem --network host --privileged -d --restart unless-stopped leds-service
    