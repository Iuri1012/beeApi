# BeeAPI v2.0 - API Documentation

## Overview

BeeAPI v2.0 is a complete rewrite that introduces a multi-user, hierarchical structure for beekeeping management.

## Architecture

The API follows this hierarchy:
```
User
  └── Apiary (multiple)
      └── Hive (multiple)
          ├── Queen Bee (one active, historical tracking)
          ├── Events Register (ordered by date)
          └── Telemetry Data
      └── Events Register (ordered by date)
```

## Data Models

### User
- `id`: Integer (auto-generated)
- `email`: String (unique, validated)
- `name`: String
- `created_at`: Timestamp
- `updated_at`: Timestamp (optional)

### Apiary
- `id`: Integer (auto-generated)
- `name`: String
- `location`: String (optional)
- `user_id`: Integer (foreign key)
- `created_at`: Timestamp
- `updated_at`: Timestamp (optional)

### Hive
- `id`: Integer (auto-generated)
- `device_id`: String (unique, for IoT device)
- `name`: String (optional)
- `apiary_id`: Integer (foreign key)
- `current_queen_id`: Integer (foreign key, nullable)
- `created_at`: Timestamp
- `updated_at`: Timestamp (optional)

### Queen Bee
- `id`: Integer (auto-generated)
- `name`: String (optional)
- `breed`: String (optional)
- `birth_date`: Timestamp (optional)
- `introduced_date`: Timestamp (auto-set)
- `retired_date`: Timestamp (nullable)
- `hive_id`: Integer (foreign key)

### Event
- `id`: Integer (auto-generated)
- `date`: Timestamp (auto-set)
- `description`: Text
- `hive_id`: Integer (foreign key, nullable)
- `apiary_id`: Integer (foreign key, nullable)
- Note: Either `hive_id` OR `apiary_id` must be set, not both

### Telemetry Reading
- `time`: Timestamp
- `device_id`: String
- `temperature`: Float (optional)
- `humidity`: Float (optional)
- `weight`: Float (optional)
- `sound_level`: Float (optional)

## API Endpoints

### User Management

#### Create User
- **POST** `/users`
- Body: `{ "email": "user@example.com", "name": "John Doe", "password": "secret" }`
- Returns: User object

#### Get All Users
- **GET** `/users`
- Returns: Array of User objects

#### Get User by ID
- **GET** `/users/{user_id}`
- Returns: User object

#### Update User
- **PUT** `/users/{user_id}`
- Body: `{ "email": "...", "name": "...", "password": "..." }` (all optional)
- Returns: Updated User object

#### Delete User
- **DELETE** `/users/{user_id}`
- Returns: Success message
- Note: Cascades to all apiaries, hives, queens, and events

---

### Apiary Management

#### Create Apiary
- **POST** `/apiaries`
- Body: `{ "name": "My Apiary", "location": "123 Main St", "user_id": 1 }`
- Returns: Apiary object

#### Get All Apiaries
- **GET** `/apiaries?user_id={user_id}` (user_id optional)
- Returns: Array of Apiary objects

#### Get Apiary by ID
- **GET** `/apiaries/{apiary_id}`
- Returns: Apiary object

#### Update Apiary
- **PUT** `/apiaries/{apiary_id}`
- Body: `{ "name": "...", "location": "..." }` (all optional)
- Returns: Updated Apiary object

#### Delete Apiary
- **DELETE** `/apiaries/{apiary_id}`
- Returns: Success message
- Note: Cascades to all hives and related data

---

### Hive Management

#### Create Hive
- **POST** `/hives`
- Body: `{ "device_id": "hive-001", "name": "Alpha Hive", "apiary_id": 1 }`
- Returns: Hive object

#### Get All Hives
- **GET** `/hives?apiary_id={apiary_id}` (apiary_id optional)
- Returns: Array of Hive objects

#### Get Hive by ID
- **GET** `/hives/{hive_id}`
- Returns: Hive object

#### Update Hive
- **PUT** `/hives/{hive_id}`
- Body: `{ "device_id": "...", "name": "...", "apiary_id": ... }` (all optional)
- Returns: Updated Hive object

#### Delete Hive
- **DELETE** `/hives/{hive_id}`
- Returns: Success message
- Note: Cascades to telemetry data and events

---

### Queen Bee Management

#### Introduce Queen to Hive
- **POST** `/hives/{hive_id}/queens`
- Body: `{ "name": "Regina", "breed": "Italian", "birth_date": "2025-01-01" }` (all optional)
- Returns: QueenBee object
- Note: Automatically retires the current queen if one exists

#### Get All Queens for a Hive
- **GET** `/hives/{hive_id}/queens`
- Returns: Array of QueenBee objects (current and historical)

#### Get Queen by ID
- **GET** `/queens/{queen_id}`
- Returns: QueenBee object

#### Update Queen
- **PUT** `/queens/{queen_id}`
- Body: `{ "name": "...", "breed": "...", "birth_date": "...", "retired_date": "..." }` (all optional)
- Returns: Updated QueenBee object

#### Delete Queen Record
- **DELETE** `/queens/{queen_id}`
- Returns: Success message
- Note: If this is the current queen, sets hive's current_queen_id to NULL

---

### Event Management

#### Create Hive Event
- **POST** `/hives/{hive_id}/events`
- Body: `{ "description": "Inspection completed, healthy colony" }`
- Returns: Event object

#### Get Hive Events
- **GET** `/hives/{hive_id}/events`
- Returns: Array of Event objects (ordered by date, newest first)

#### Create Apiary Event
- **POST** `/apiaries/{apiary_id}/events`
- Body: `{ "description": "Annual inspection by authority" }`
- Returns: Event object

#### Get Apiary Events
- **GET** `/apiaries/{apiary_id}/events`
- Returns: Array of Event objects (ordered by date, newest first)

#### Delete Event
- **DELETE** `/events/{event_id}`
- Returns: Success message

---

### Telemetry Management

#### Get Hive Telemetry
- **GET** `/hives/{hive_id}/telemetry?limit={limit}` (limit default: 100)
- Returns: Array of TelemetryReading objects

#### WebSocket Real-time Telemetry
- **WebSocket** `/ws/hive/{hive_id}/telemetry`
- Connects to real-time telemetry stream
- Sends last 10 readings on connect
- Sends new readings as they arrive
- Sends periodic pings to keep connection alive

---

## Example Workflow

### 1. Create a User
```bash
curl -X POST http://localhost:8000/users \
  -H "Content-Type: application/json" \
  -d '{"email": "beekeeper@example.com", "name": "John Beekeeper", "password": "secret123"}'
```

### 2. Create an Apiary
```bash
curl -X POST http://localhost:8000/apiaries \
  -H "Content-Type: application/json" \
  -d '{"name": "Sunny Valley Apiary", "location": "123 Farm Road", "user_id": 1}'
```

### 3. Create a Hive
```bash
curl -X POST http://localhost:8000/hives \
  -H "Content-Type: application/json" \
  -d '{"device_id": "hive-001", "name": "Alpha Hive", "apiary_id": 1}'
```

### 4. Introduce a Queen
```bash
curl -X POST http://localhost:8000/hives/1/queens \
  -H "Content-Type: application/json" \
  -d '{"name": "Regina Prima", "breed": "Italian", "birth_date": "2025-01-15"}'
```

### 5. Add an Event
```bash
curl -X POST http://localhost:8000/hives/1/events \
  -H "Content-Type: application/json" \
  -d '{"description": "First inspection - colony looks strong"}'
```

### 6. Get Telemetry
```bash
curl http://localhost:8000/hives/1/telemetry?limit=50
```

## Database Schema

The application uses a dual-database architecture for optimal performance:

### PostgreSQL (Main Database)
Stores all relational/entity data:
- `users` - User accounts
- `apiaries` - Apiaries owned by users
- `hives` - Hives within apiaries
- `queen_bees` - Queen bees (current and historical)
- `events` - Event logs for hives and apiaries

**Port:** 5432  
**Database:** `beeapi`

### TimescaleDB (Time-Series Database)
Stores only high-frequency time-series data:
- `readings` - Telemetry data (TimescaleDB hypertable)
- `readings_hourly` - Continuous aggregate for hourly averages

**Port:** 5433  
**Database:** `beeapi_telemetry`

### Why Two Databases?

- **PostgreSQL** is optimized for:
  - CRUD operations on entities
  - Complex joins and relationships
  - Transaction management
  - User data and business logic

- **TimescaleDB** is optimized for:
  - High-frequency sensor readings
  - Time-based queries and aggregations
  - Data compression
  - Retention policies

All foreign key relationships in PostgreSQL have CASCADE delete, so deleting a user will remove all their data. The TimescaleDB readings reference device_id but don't enforce foreign keys across databases.

## Migration from v1.0

The v2.0 schema is **not backward compatible** with v1.0. To migrate:

1. Back up your existing data
2. Create a user for your existing data
3. Create an apiary for that user
4. Migrate existing hives to the new apiary
5. Update your device firmware to use the new API endpoints

## Notes

- **Security**: This version still uses plaintext passwords. In production, implement proper password hashing (bcrypt, argon2, etc.)
- **Authentication**: No authentication is implemented yet. Add JWT or session-based auth for production
- **Authorization**: No user-level authorization. Users can currently access all data
- **Validation**: Basic validation is in place, but add more business logic as needed
