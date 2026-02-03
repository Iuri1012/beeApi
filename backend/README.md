# Backend API

FastAPI-based REST API for beehive monitoring.

## Installation

```bash
pip install -r requirements.txt
```

## Running

```bash
uvicorn main:app --reload
```

API will be available at http://localhost:8000
API documentation at http://localhost:8000/docs

## Endpoints

- `POST /register-device` - Register a new device
- `GET /hives` - List all hives
- `GET /hives/{device_id}` - Get specific hive
- `GET /hives/{device_id}/telemetry` - Get telemetry history
- `WS /ws/hive/{device_id}/telemetry` - Real-time telemetry WebSocket
