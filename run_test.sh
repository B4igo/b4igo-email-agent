#!/bin/bash
# Helper script to run the workflow test with the correct Python interpreter

VENV_PYTHON="/home/err/repo/.venv/bin/python"

if [ ! -f "$VENV_PYTHON" ]; then
    echo "Error: Virtual environment Python not found at $VENV_PYTHON"
    echo "Please check your virtual environment path."
    exit 1
fi

echo "Using Python: $VENV_PYTHON"
echo "Running test_workflow.py..."
echo ""

"$VENV_PYTHON" test_workflow.py "$@"
