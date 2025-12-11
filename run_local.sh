#!/usr/bin/env bash
set -e

export APP_ENV=local
uvicorn backend.app:app --reload --host 0.0.0.0 --port 8000
