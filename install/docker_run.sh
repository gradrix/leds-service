#!/bin/bash

docker run --name ledserver -it --device /dev/gpiomem -v "/home/pi/leds-service:/usr/src/app" -p 800:800 --privileged -d --restart unless-stopped gradrix/ledserver 
