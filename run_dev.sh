#!/usr/bin/env bash
# Runs the real images on this machine with a simulated strip (LED_DRIVER=sim): http://localhost:8080
# ./run_dev.sh stop    removes the containers again.
set -euo pipefail
cd "$(dirname "$0")"
port="${LEDS_DEV_PORT:-8080}"

docker rm -f leds-dev-web leds-dev-gpio >/dev/null 2>&1 || true
[ "${1:-}" = stop ] && { docker network rm leds-dev >/dev/null 2>&1 || true; exit 0; }

docker build -q -t leds-gpio:dev -f docker/gpio_service/Dockerfile . >/dev/null
docker build -q -t leds-web:dev -f docker/web_api/Dockerfile . >/dev/null
docker network create leds-dev >/dev/null 2>&1 || true
docker run -d --rm --name leds-dev-gpio --network leds-dev --tmpfs /state -e LED_DRIVER=sim \
  -e LED_COUNT="${LED_COUNT:-360}" leds-gpio:dev >/dev/null
docker run -d --rm --name leds-dev-web --network leds-dev -e GPIO_SERVICE_ADDRESS=leds-dev-gpio:9000 \
  -p "$port:80" leds-web:dev >/dev/null
echo "http://localhost:$port"
