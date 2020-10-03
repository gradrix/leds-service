#!/bin/bash

currentDir=$(pwd)
serviceFile=$currentDir/leds.service

echo "copying $serviceFile"
sudo cp $serviceFile /etc/systemd/system/

echo "Enabling servicee"
sudo systemctl enable leds

echo "Restarting service"
sudo systemctl restart leds

sudo systemctl status leds
