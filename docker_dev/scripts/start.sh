#!/bin/bash
cd /src
uvicorn indexer.api.app:app --reload --workers 1 --host 0.0.0.0 --port 8000