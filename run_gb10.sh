#!/usr/bin/env bash
set -e

export APP_ENV=gb10
export OPENCV_LOG_LEVEL=ERROR

uvicorn backend.app:app --host 0.0.0.0 --port 8000


#chmod +x scripts/run_local.sh scripts/run_gb10.sh