#!/bin/bash
set -e
echo "Starting Real-Time Crypto Portfolio Analyzer..."
uvicorn app:app --host 0.0.0.0 --port 9030 --workers 1
