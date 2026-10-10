#!/usr/bin/env bash

set -euo pipefail

TARGET_URL="${1:-http://localhost:8000/v1/predict}"
TOTAL_REQUESTS="${2:-500}"
CONCURRENCY="${3:-10}"

echo ">>> Starting Benchmark on: ${TARGET_URL}"
echo ">>> Total requests: ${TOTAL_REQUESTS}, Concurrency: ${CONCURRENCY}"

PAYLOAD='{"features": [5.1, 3.5, 1.4, 0.2]}'

if which hey &>/dev/null; then
    hey -n "${TOTAL_REQUESTS}" -c "${CONCURRENCY}" -m POST -H "Content-Type: application/json" -d "${PAYLOAD}" "${TARGET_URL}"
else
    START_TIME=$(date +%s%N)
    for i in $(seq 1 "${TOTAL_REQUESTS}"); do
        curl -s -X POST "${TARGET_URL}" -H "Content-Type: application/json" -d "${PAYLOAD}" > /dev/null
    done
    END_TIME=$(date +%s%N)
    DURATION=$(( (END_TIME - START_TIME) / 1000000 ))
    echo "Completed ${TOTAL_REQUESTS} requests in ${DURATION} ms."
fi

echo ">>> Memory Footprint:"
free -h
