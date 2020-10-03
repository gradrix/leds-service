#!/bin/bash

./docker_build.sh
./docker_run.sh

docker stop ledserver

./install_service.sh
