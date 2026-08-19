#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${BASE_URL:-http://localhost:9090}"

health_payload="$(curl --fail --silent --show-error "$BASE_URL/actuator/health")"
grep -q '"status"[[:space:]]*:[[:space:]]*"UP"' <<<"$health_payload"

openapi_payload="$(curl --fail --silent --show-error "$BASE_URL/v3/api-docs")"
grep -q '"openapi"' <<<"$openapi_payload"

root_status="$(curl --silent --output /dev/null --write-out '%{http_code}' "$BASE_URL/")"
case "$root_status" in
  200|302) ;;
  *) echo "Unexpected root status: $root_status" >&2; exit 1 ;;
esac

echo "Smoke checks passed for $BASE_URL"
