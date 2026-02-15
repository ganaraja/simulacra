#!/usr/bin/env bash
# Run all tests (backend + frontend). Exit 1 if any fail.
set -e
cd "$(dirname "$0")/.."
echo "=== Backend tests (pytest) ==="
PYTHONPATH=src python3 -m pytest tests/ -v
echo ""
echo "=== Frontend tests (Jest) ==="
cd src/frontend && npm run test && cd ../..
echo ""
echo "All tests passed."
