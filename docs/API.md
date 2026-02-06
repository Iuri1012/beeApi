# BeeAPI REST API Documentation

## Overview

The BeeAPI provides a RESTful API for managing beehive data, telemetry, and events. This API supports full CRUD operations for beehives, events, and telemetry data collection.

## Base URL

```
http://localhost:8000
```

## Authentication

The API uses Firebase Authentication for securing endpoints. Include the Firebase ID token in the Authorization header:

```
Authorization: Bearer <firebase-id-token>
```

## API Endpoints

### Health Check

#### GET /health
Returns the health status of the API.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T00:00:00Z"
}
```

### Beehives

#### GET /beehives
Get all beehives for the authenticated user.

**Response:**
```json
[
  {
    "id": "uuid",
    "name": "Hive 001",
    "location": "Garden North",
    "created_at": "2024-01-01T00:00:00Z",
    "user_id": "user-uuid"
  }
]
```

#### POST /beehives
Create a new beehive.

**Request Body:**
```json
{
  "name": "Hive 002",
  "location": "Garden South"
}
```

**Response:**
```json
{
  "id": "uuid",
  "name": "Hive 002",
  "location": "Garden South",
  "created_at": "2024-01-01T00:00:00Z",
  "user_id": "user-uuid"
}
```

#### PUT /beehives/{beehive_id}
Update an existing beehive.

**Request Body:**
```json
{
  "name": "Updated Hive Name",
  "location": "Updated Location"
}
```

#### DELETE /beehives/{beehive_id}
Delete a beehive.

**Response:**
```json
{
  "message": "Beehive deleted successfully"
}
```

### Events

#### GET /events
Get all events for the authenticated user's beehives.

**Query Parameters:**
- `beehive_id` (optional): Filter events by beehive ID

**Response:**
```json
[
  {
    "id": "uuid",
    "beehive_id": "uuid",
    "event_type": "inspection",
    "description": "Routine hive inspection",
    "timestamp": "2024-01-01T00:00:00Z"
  }
]
```

#### POST /events
Create a new event.

**Request Body:**
```json
{
  "beehive_id": "uuid",
  "event_type": "inspection",
  "description": "Routine hive inspection"
}
```

#### PUT /events/{event_id}
Update an existing event.

**Request Body:**
```json
{
  "event_type": "treatment",
  "description": "Applied varroa treatment"
}
```

#### DELETE /events/{event_id}
Delete an event.

**Response:**
```json
{
  "message": "Event deleted successfully"
}
```

### Telemetry

#### GET /telemetry
Get telemetry data for beehives.

**Query Parameters:**
- `beehive_id` (optional): Filter by beehive ID
- `start_date` (optional): Start date for time range (ISO 8601)
- `end_date` (optional): End date for time range (ISO 8601)
- `limit` (optional): Maximum number of records (default: 100)

**Response:**
```json
[
  {
    "device_id": "hive-001",
    "timestamp": "2024-01-01T00:00:00Z",
    "temperature": 35.2,
    "humidity": 65.8,
    "weight": 45.6,
    "sound_level": 42.1
  }
]
```

#### GET /telemetry/latest/{device_id}
Get the latest telemetry reading for a specific device.

**Response:**
```json
{
  "device_id": "hive-001",
  "timestamp": "2024-01-01T00:00:00Z",
  "temperature": 35.2,
  "humidity": 65.8,
  "weight": 45.6,
  "sound_level": 42.1
}
```

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Validation error message"
}
```

### 401 Unauthorized
```json
{
  "detail": "Invalid or missing authentication token"
}
```

### 403 Forbidden
```json
{
  "detail": "Access denied"
}
```

### 404 Not Found
```json
{
  "detail": "Resource not found"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

## Data Models

### Beehive
```json
{
  "id": "string (UUID)",
  "name": "string",
  "location": "string",
  "created_at": "string (ISO 8601)",
  "user_id": "string (UUID)"
}
```

### Event
```json
{
  "id": "string (UUID)",
  "beehive_id": "string (UUID)",
  "event_type": "string",
  "description": "string",
  "timestamp": "string (ISO 8601)"
}
```

### Telemetry
```json
{
  "device_id": "string",
  "timestamp": "string (ISO 8601)",
  "temperature": "number",
  "humidity": "number",
  "weight": "number",
  "sound_level": "number"
}
```

## Interactive Documentation

When the API is running, you can access the interactive OpenAPI documentation at:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Rate Limiting

The API implements basic rate limiting to prevent abuse. If you exceed the rate limit, you'll receive a 429 status code.

## MQTT Integration

The API integrates with MQTT for real-time telemetry data ingestion. Devices should publish to:

**Topic Pattern:** `telemetry/{device_id}`

**Payload Format:**
```json
{
  "device_id": "hive-001",
  "timestamp": "2024-01-01T00:00:00Z",
  "temperature": 35.2,
  "humidity": 65.8,
  "weight": 45.6,
  "sound_level": 42.1
}
```

## WebSocket Support

Real-time telemetry updates are available via WebSocket at:

```
ws://localhost:8000/ws/telemetry
```

The WebSocket sends real-time telemetry data as JSON messages in the same format as the REST API.