#!/bin/bash
export LED_COUNT=360
export LED_PORT=9000
export LED_PIN=18

sudo python3 ./gpio-service/app/main.py
