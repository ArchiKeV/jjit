#!/bin/bash
source venv/bin/activate
uvicorn --app-dir=./app/ main:app --host 127.0.0.1 --port 8000 --reload
