#!/bin/bash
currentDir=$(pwd)

#Build
echo "Building docker images"
docker-compose build

#Create network
echo "Attempting to create a Docker network (if not exists)"
docker network create --driver bridge leds-network || true

#Run
#docker-compose up
echo "Adding service file to systemd"
cat << EOF | sudo tee /lib/systemd/system/leds-web.service
[Unit]
Description=Leds-Web Service
After=network.target docker.service

[Service]
WorkingDirectory=$currentDir
Type=simple
Restart=always
ExecStart=/usr/local/bin/docker-compose up --remove-orphans
ExecStop=/usr/local/bin/docker-compose down --remove-orphans

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload

sudo systemctl enable leds-web

sudo systemctl start leds-web

sudo systemctl status leds-web
