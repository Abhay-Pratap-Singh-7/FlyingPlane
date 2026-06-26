#!/bin/bash
cd "$(dirname "$0")"

# Kill any existing processes using ports 9000 and 8765
pids=$(lsof -t -i :9000 -i :8765)
if [ ! -z "$pids" ]; then
    kill -9 $pids 2>/dev/null || true
fi

if [ ! -d "venv" ]; then
    python3 -m venv venv
    ./venv/bin/pip install websockets
fi
./venv/bin/python3 web_bridge.py
