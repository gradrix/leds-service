#!/bin/bash

pip3 install grpcio-tools

python3 -m grpc_tools.protoc -I=gpio_api --python_out=./ --grpc_python_out=./ gpio_api/led_service.proto