#!/bin/bash

docker build -t react-build -f docker/ui/Dockerfile .

docker run --rm -v $(pwd)/frontend_build:/frontend_build react-build