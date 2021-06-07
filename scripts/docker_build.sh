#!/bin/bash

#Creating image
docker build -t gradrix/ledserver .

#Running container & creating it (by doing it)
docker run --name ledserver -it --device /dev/gpiomem -p 9000:9000 --privileged -d --restart unless-stopped --network leds-network gradrix/ledserver
