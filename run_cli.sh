#!/bin/bash
echo "Starting HydroBuddy in CLI mode..."
source .venv/bin/activate 2>/dev/null || true
python3 hydrobuddy.py cli