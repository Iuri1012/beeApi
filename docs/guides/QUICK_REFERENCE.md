# BeeAPI v2.0 - Quick Reference

## Data Hierarchy
```
User → Apiary → Hive → Queen Bee
                   ├── Events
                   └── Telemetry
         └── Events
```

## Core Endpoints

### Users
```
POST   /users                    Create user
GET    /users                    List users
GET    /users/{id}               Get user
PUT    /users/{id}               Update user
DELETE /users/{id}               Delete user
```

### Apiaries
```
POST   /apiaries                 Create apiary
GET    /apiaries?user_id={id}    List apiaries
GET    /apiaries/{id}            Get apiary
PUT    /apiaries/{id}            Update apiary
DELETE /apiaries/{id}            Delete apiary
```

### Hives
```
POST   /hives                    Create hive
GET    /hives?apiary_id={id}     List hives
GET    /hives/{id}               Get hive
PUT    /hives/{id}               Update hive
DELETE /hives/{id}               Delete hive
```

### Queen Bees
```
POST   /hives/{id}/queens        Introduce queen
GET    /hives/{id}/queens        List queens
GET    /queens/{id}              Get queen
PUT    /queens/{id}              Update queen
DELETE /queens/{id}              Delete queen
```

### Events
```
POST   /hives/{id}/events        Add hive event
GET    /hives/{id}/events        Get hive events
POST   /apiaries/{id}/events     Add apiary event
GET    /apiaries/{id}/events     Get apiary events
DELETE /events/{id}              Delete event
```

### Telemetry
```
GET    /hives/{id}/telemetry     Get readings
WS     /ws/hive/{id}/telemetry   Real-time stream
```

## Quick Start

### 1. Create User
```bash
curl -X POST http://localhost:8000/users \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","name":"John Doe","password":"secret"}'
```

### 2. Create Apiary
```bash
curl -X POST http://localhost:8000/apiaries \
  -H "Content-Type: application/json" \
  -d '{"name":"My Apiary","location":"123 Main St","user_id":1}'
```

### 3. Create Hive
```bash
curl -X POST http://localhost:8000/hives \
  -H "Content-Type: application/json" \
  -d '{"device_id":"hive-001","name":"Alpha","apiary_id":1}'
```

### 4. Add Queen
```bash
curl -X POST http://localhost:8000/hives/1/queens \
  -H "Content-Type: application/json" \
  -d '{"name":"Regina","breed":"Italian"}'
```

### 5. Add Event
```bash
curl -X POST http://localhost:8000/hives/1/events \
  -H "Content-Type: application/json" \
  -d '{"description":"Inspection complete - healthy colony"}'
```

## Data Models

### User
- email (required, unique)
- name (required)
- password (required)

### Apiary
- name (required)
- location (optional)
- user_id (required)

### Hive
- device_id (required, unique)
- name (optional)
- apiary_id (required)

### Queen Bee
- name (optional)
- breed (optional)
- birth_date (optional)

### Event
- description (required)
- Either hive_id OR apiary_id (required)

## Important Notes

⚠️ **Cascade Deletes:**
- Delete User → deletes all Apiaries, Hives, Queens, Events
- Delete Apiary → deletes all Hives and related data
- Delete Hive → deletes all Queens, Events, Telemetry

⚠️ **Security:**
- No authentication implemented yet
- Passwords stored in plaintext (DO NOT use in production)
- All users can access all data

⚠️ **Queen Management:**
- Introducing new queen auto-retires current queen
- History is preserved (retired_date is set)

## Testing

### Interactive Docs
```
http://localhost:8000/docs
```

### Test Script
```bash
cd backend
python test_api.py
```

## Common Queries

### Get user's apiaries
```bash
curl http://localhost:8000/apiaries?user_id=1
```

### Get apiary's hives
```bash
curl http://localhost:8000/hives?apiary_id=1
```

### Get hive's queen history
```bash
curl http://localhost:8000/hives/1/queens
```

### Get recent hive events
```bash
curl http://localhost:8000/hives/1/events
```

### Get telemetry (last 100 readings)
```bash
curl http://localhost:8000/hives/1/telemetry?limit=100
```

## Files & Structure

```
backend/
├── main.py              # App entry point
├── models/
│   ├── user_models.py   # User models
│   └── bee_models.py    # Apiary, Hive, Queen, Event
└── controllers/
    ├── user_controller.py  # User endpoints
    └── bee_controller.py   # Bee endpoints
```

## Running the App

```bash
# Start both databases
docker-compose up -d postgres timescaledb

# Install dependencies
cd backend
pip install -r requirements.txt

# Run the app
python main.py

# Or with auto-reload
uvicorn main:app --reload
```

## Database Architecture

**PostgreSQL (5432):** Users, Apiaries, Hives, Queens, Events  
**TimescaleDB (5433):** Telemetry readings (time-series)

See `/DATABASE_ARCHITECTURE.md` for details.

## Documentation

- **API Documentation:** `/backend/API_V2.md`
- **Migration Guide:** `/backend/MIGRATION_GUIDE.md`
- **Update Summary:** `/UPDATE_SUMMARY.md`
- **Interactive Docs:** `http://localhost:8000/docs`
