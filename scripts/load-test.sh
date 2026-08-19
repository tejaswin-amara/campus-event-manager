#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${BASE_URL:-http://localhost:9090}"
REQUESTS="${REQUESTS:-100}"
CONCURRENCY="${CONCURRENCY:-10}"
TARGET_URL="${TARGET_URL:-$BASE_URL/actuator/health}"

start_ns="$(date +%s%N)"
failures=0

if ! seq 1 "$REQUESTS" | xargs -P "$CONCURRENCY" -I '{}' sh -c 'curl --fail --silent --show-error --output /dev/null "$0"' "$TARGET_URL"; then
  failures=1
fi

end_ns="$(date +%s%N)"
elapsed_ms=$(( (end_ns - start_ns) / 1000000 ))
if [ "$elapsed_ms" -eq 0 ]; then elapsed_ms=1; fi
throughput=$(awk -v requests="$REQUESTS" -v elapsed="$elapsed_ms" 'BEGIN { printf "%.2f", requests / (elapsed / 1000) }')

printf 'target=%s requests=%s concurrency=%s elapsed_ms=%s throughput_rps=%s failures=%s\n' \
  "$TARGET_URL" "$REQUESTS" "$CONCURRENCY" "$elapsed_ms" "$throughput" "$failures"

[ "$failures" -eq 0 ]
