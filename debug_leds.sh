#!/bin/bash
export LED_COUNT=50
export LED_PORT=9000
export LED_PIN=18

sudo -E python3 ./gpio-service/app/main.py
