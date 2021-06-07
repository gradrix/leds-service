#!/bin/bash

#Run
echo "Adding service file to systemd"
cat << EOF | sudo tee /lib/systemd/system/leds.service
[Unit]
Description=Leds service
Requires=docker.service
After=docker.service

[Service]
Restart=always
ExecStart=/usr/bin/docker start -a ledserver
ExecStop=/usr/bin/docker stop -t 2 ledserver

[Install]
WantedBy=default.target
EOF

sudo systemctl daemon-reload

echo "Enabling servicee"
sudo systemctl enable leds

echo "Restarting service"
sudo systemctl start leds

sudo systemctl status leds
