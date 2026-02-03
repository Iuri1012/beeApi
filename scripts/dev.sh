#!/bin/bash

# Local Development Helper
# Runs individual components without Docker for development

set -e

function show_help() {
    cat << EOF
BeeAPI Local Development Helper

Usage: ./scripts/dev.sh [component]

Components:
  backend     - Start FastAPI backend (requires postgres)
  telemetry   - Start telemetry consumer (requires postgres & mosquitto)
  web         - Start React development server
  simulator   - Start firmware simulator
  all         - Show instructions for running all components

Prerequisites:
  - PostgreSQL with TimescaleDB running
  - MQTT broker (Mosquitto) running
  - Python 3.9+
  - Node.js 16+

EOF
}

function setup_backend() {
    echo "Setting up Backend..."
    cd backend
    
    if [ ! -d "venv" ]; then
        python3 -m venv venv
        source venv/bin/activate
        pip install -r requirements.txt
    else
        source venv/bin/activate
    fi
    
    export DATABASE_URL="postgresql://beeapi:beeapi123@localhost:5432/beeapi"
    export MQTT_BROKER="localhost"
    export MQTT_PORT="1883"
    
    echo "Starting backend on http://localhost:8000"
    echo "API docs: http://localhost:8000/docs"
    uvicorn main:app --reload
}

function setup_telemetry() {
    echo "Setting up Telemetry Consumer..."
    cd telemetry
    
    if [ ! -d "venv" ]; then
        python3 -m venv venv
        source venv/bin/activate
        pip install -r requirements.txt
    else
        source venv/bin/activate
    fi
    
    export DATABASE_URL="postgresql://beeapi:beeapi123@localhost:5432/beeapi"
    export MQTT_BROKER="localhost"
    export MQTT_PORT="1883"
    
    echo "Starting telemetry consumer..."
    python consumer.py
}

function setup_web() {
    echo "Setting up Web Dashboard..."
    cd web
    
    if [ ! -d "node_modules" ]; then
        npm install
    fi
    
    export REACT_APP_API_URL="http://localhost:8000"
    export REACT_APP_WS_URL="ws://localhost:8000"
    
    echo "Starting web dashboard on http://localhost:3000"
    npm start
}

function setup_simulator() {
    echo "Setting up Firmware Simulator..."
    cd firmware
    
    if [ ! -d "venv" ]; then
        python3 -m venv venv
        source venv/bin/activate
        pip install -r requirements.txt
    else
        source venv/bin/activate
    fi
    
    echo "Starting simulator..."
    python simulator.py --device-id hive-001 --broker localhost --interval 5
}

function show_all() {
    cat << EOF

To run all components locally, you need to:

1. Start PostgreSQL with TimescaleDB:
   docker run -d --name beeapi-postgres \\
     -e POSTGRES_DB=beeapi \\
     -e POSTGRES_USER=beeapi \\
     -e POSTGRES_PASSWORD=beeapi123 \\
     -p 5432:5432 \\
     -v $(pwd)/timeseries/init.sql:/docker-entrypoint-initdb.d/init.sql \\
     timescale/timescaledb:latest-pg15

2. Start Mosquitto:
   docker run -d --name beeapi-mosquitto \\
     -p 1883:1883 \\
     -v $(pwd)/docker/mosquitto/mosquitto.conf:/mosquitto/config/mosquitto.conf \\
     eclipse-mosquitto:2

3. Start backend (Terminal 1):
   ./scripts/dev.sh backend

4. Start telemetry consumer (Terminal 2):
   ./scripts/dev.sh telemetry

5. Start web dashboard (Terminal 3):
   ./scripts/dev.sh web

6. Start simulator (Terminal 4):
   ./scripts/dev.sh simulator

EOF
}

case "${1}" in
    backend)
        setup_backend
        ;;
    telemetry)
        setup_telemetry
        ;;
    web)
        setup_web
        ;;
    simulator)
        setup_simulator
        ;;
    all)
        show_all
        ;;
    *)
        show_help
        ;;
esac
