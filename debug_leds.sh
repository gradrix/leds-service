#!/bin/bash
export LED_COUNT=360
export LED_PORT=$2
export LED_PIN=$1

sudo -E python3 ./gpio-service/main.py
