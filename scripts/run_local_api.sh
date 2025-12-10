#!/usr/bin/env bash
set -e

# Activate venv if present
if [ -d ".venv" ]; then
  source .venv/bin/activate
fi

export PYTHONPATH=.

uvicorn src.app.main_api:app --host 0.0.0.0 --port 8000
