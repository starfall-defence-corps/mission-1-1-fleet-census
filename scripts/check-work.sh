#!/usr/bin/env bash
set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"
TEST_FILE="$ROOT_DIR/molecule/default/tests/test_fleet_inspection.py"

echo ""
echo "=============================================="
echo "  ARIA - Automated Review & Intelligence Analyst"
echo "  Running Mission 1.1 Verification..."
echo "=============================================="
echo ""

cd "$ROOT_DIR"

# Activate project venv if it exists
if [ -f "$ROOT_DIR/venv/bin/activate" ]; then
    source "$ROOT_DIR/venv/bin/activate"
fi

python3 -m pytest "$TEST_FILE" -v --tb=short 2>&1 | \
    sed 's/PASSED/VERIFIED/g' | \
    sed 's/FAILED/DEFICIENCY DETECTED/g'

EXIT_CODE=${PIPESTATUS[0]}

echo ""
if [ $EXIT_CODE -eq 0 ]; then
    echo "=============================================="
    echo "  ARIA: All objectives verified."
    echo "  Mission 1.1 status: COMPLETE"
    echo ""
    echo "  Cadet, you have inspected the fleet."
    echo "  The Starfall Defence Corps acknowledges"
    echo "  your contribution to fleet security."
    echo "=============================================="
else
    echo "=============================================="
    echo "  ARIA: Deficiencies detected."
    echo "  Review the output above and correct."
    echo "  Run 'make test' again when ready."
    echo "=============================================="
fi

echo ""
exit $EXIT_CODE
