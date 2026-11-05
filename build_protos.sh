#!/usr/bin/env bash
# Regenerates gpio_api/*_pb2*.py. Tool versions match requirements.txt.
set -euo pipefail
cd "$(dirname "$0")"
docker run --rm -v "$PWD:/src" -w /src --user "$(id -u):$(id -g)" -e HOME=/tmp python:3.11-slim-bookworm sh -c '
  pip install -q --no-warn-script-location --target /tmp/tools grpcio-tools==1.66.2 protobuf==5.28.3 &&
  PYTHONPATH=/tmp/tools python -m grpc_tools.protoc -Igpio_api --python_out=. --grpc_python_out=. gpio_api/gpio_api/led_service.proto'
