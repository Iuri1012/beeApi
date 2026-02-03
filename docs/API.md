# API Documentation

## Base URL

Development: `http://localhost:8000`

## Authentication

Currently no authentication is implemented (PoC only).

## Endpoints

### Health Check

#### GET /
Returns API status and version.

**Response:**
```json
{
  "message": "BeeAPI - Beehive Monitoring System",
  "version": "1.0.0"
}
```

### Device Management

#### POST /register-device
Register a new beehive device.

**Request Body:**
```json
{
  "device_id": "hive-001",
  "name": "Hive Alpha",
  "location": "Apiary A"
}
```

**Response:** (201 Created)
```json
{
  "id": 1,
  "device_id": "hive-001",
  "name": "Hive Alpha",
  "location": "Apiary A",
  "registered_at": "2026-02-03T13:00:00Z"
}
```

#### GET /hives
Get all registered hives.

**Response:**
```json
[
  {
    "id": 1,
    "device_id": "hive-001",
    "name": "Hive Alpha",
    "location": "Apiary A",
    "registered_at": "2026-02-03T13:00:00Z"
  }
]
```

#### GET /hives/{device_id}
Get a specific hive.

**Response:**
```json
{
  "id": 1,
  "device_id": "hive-001",
  "name": "Hive Alpha",
  "location": "Apiary A",
  "registered_at": "2026-02-03T13:00:00Z"
}
```

### Telemetry

#### GET /hives/{device_id}/telemetry
Get telemetry history for a hive.

**Query Parameters:**
- `limit`: Number of records (default: 100)

**Response:**
```json
[
  {
    "time": "2026-02-03T13:00:00Z",
    "device_id": "hive-001",
    "temperature": 35.5,
    "humidity": 62.3,
    "weight": 45.2,
    "sound_level": 48.7
  }
]
```

#### WS /ws/hive/{device_id}/telemetry
WebSocket endpoint for real-time telemetry.

**Message Format:**
```json
{
  "time": "2026-02-03T13:00:00Z",
  "device_id": "hive-001",
  "temperature": 35.5,
  "humidity": 62.3,
  "weight": 45.2,
  "sound_level": 48.7
}
```

## MQTT Topics

### Telemetry Publishing

**Topic:** `beehive/{device_id}/telemetry`

**Payload:**
```json
{
  "device_id": "hive-001",
  "timestamp": "2026-02-03T13:00:00Z",
  "temperature": 35.5,
  "humidity": 62.3,
  "weight": 45.2,
  "sound_level": 48.7
}
```
