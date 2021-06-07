#!/bin/bash

#Stop & delete existing container
echo "Stopping and removing existing container (if exists):"
docker stop ledserver || true && docker rm ledserver || true

#Create network
echo "Creating docker network (if does not exists):"
docker network create --driver bridge leds-network || true

#Build and create container by running it once
./scripts/docker_build.sh

#Stop container and install service
docker stop ledserver
./scripts/install_service.sh
