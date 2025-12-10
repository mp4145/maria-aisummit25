    #!/usr/bin/env bash
# Placeholder: when you're on the GB10 box, you can:
# - create venv
# - pip install -r requirements.txt
# - run the API
set -e

export PYTHONPATH=.

uvicorn src.app.main_api:app --host 0.0.0.0 --port 8000
