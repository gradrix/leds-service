#!/bin/bash

pip3 install grpcio-tools

python3 -m grpc_tools.protoc -I=. --python_out=./ --grpc_python_out=./ api/led_service.proto