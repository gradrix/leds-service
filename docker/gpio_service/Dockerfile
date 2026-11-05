FROM python:3.11-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

# rpi_ws281x builds its C extension from source.
COPY ./gpio_service/requirements.txt .
RUN apt-get update && apt-get install -y --no-install-recommends gcc libc6-dev \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get purge -y gcc libc6-dev && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

# Strip configuration; override at run time.
ENV LED_PORT=9000 LED_PIN=18 LED_COUNT=360 LEDS_STATE_FILE=/state/saved-data

WORKDIR /app
COPY ./gpio_api ./gpio_api
COPY ./gpio_service ./gpio_service

EXPOSE 9000
CMD ["python", "-m", "gpio_service.main"]
