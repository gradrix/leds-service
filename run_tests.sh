#!/usr/bin/env bash
# Hardware-free unit tests in a disposable container (no GPIO, no network).
set -euo pipefail
cd "$(dirname "$0")"
image="leds-service-tests:py3.11"
docker build -q -t "$image" -f tests/Dockerfile tests >/dev/null
docker run --rm --network none -v "$PWD:/src:ro" -e PYTHONDONTWRITEBYTECODE=1 "$image" tests "$@"
