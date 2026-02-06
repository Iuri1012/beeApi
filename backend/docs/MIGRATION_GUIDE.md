# BeeAPI v2.0 - Migration and Setup Guide

## What's New in v2.0

### Major Changes
1. **Multi-User Support**: The system now supports multiple users, each with their own apiaries
2. **Hierarchical Structure**: User → Apiary → Hive → Queen Bee
3. **Queen Bee Management**: Track current and historical queens for each hive
4. **Event Logging**: Separate event registers for both hives and apiaries
5. **Organized Controllers**: Code separated into `user_controller` and `bee_controller`
6. **Better Data Models**: Pydantic models organized in separate modules

### Database Schema Changes
- **New Tables**:
  - `users` - User management
  - `apiaries` - Apiary management
  - `queen_bees` - Queen bee tracking
  - `events` - Event logging for hives and apiaries
  
- **Modified Tables**:
  - `hives` - Now includes `apiary_id`, `current_queen_id`, removed `location`

## Setup Instructions

### 1. Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 2. Database Setup

The application uses **two databases**:
- **PostgreSQL** (port 5432): Relational data (users, apiaries, hives, queens, events)
- **TimescaleDB** (port 5433): Time-series data (telemetry readings)

If you're starting fresh:
```bash
# Start both databases with docker-compose
docker-compose up -d postgres timescaledb

# Wait for the databases to be ready, the init scripts will run automatically
# Check logs:
docker-compose logs postgres
docker-compose logs timescaledb
```

If you have existing data, you'll need to migrate:
```bash
# Backup your existing database first!
pg_dump beeapi > backup.sql

# Stop and remove old containers
docker-compose down -v

# Start fresh with the new dual-database setup
docker-compose up -d postgres timescaledb
```

### 3. Run the Application
```bash
cd backend
python main.py
```

Or with uvicorn directly:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 4. Verify Installation
Open your browser to http://localhost:8000/docs to see the interactive API documentation.

## Quick Start Example

### 1. Create a User
```bash
curl -X POST http://localhost:8000/users \
  -H "Content-Type: application/json" \
  -d '{
    "email": "beekeeper@example.com",
    "name": "John Doe",
    "password": "mypassword"
  }'
```

Response:
```json
{
  "id": 1,
  "email": "beekeeper@example.com",
  "name": "John Doe",
  "created_at": "2026-02-03T10:00:00"
}
```

### 2. Create an Apiary
```bash
curl -X POST http://localhost:8000/apiaries \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Sunny Valley Apiary",
    "location": "123 Farm Road, Rural County",
    "user_id": 1
  }'
```

### 3. Create a Hive
```bash
curl -X POST http://localhost:8000/hives \
  -H "Content-Type: application/json" \
  -d '{
    "device_id": "hive-001",
    "name": "Alpha Hive",
    "apiary_id": 1
  }'
```

### 4. Introduce a Queen Bee
```bash
curl -X POST http://localhost:8000/hives/1/queens \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Regina Prima",
    "breed": "Italian",
    "birth_date": "2025-01-15T00:00:00"
  }'
```

### 5. Add Events
```bash
# Hive event
curl -X POST http://localhost:8000/hives/1/events \
  -H "Content-Type: application/json" \
  -d '{
    "description": "First inspection - colony strong and healthy"
  }'

# Apiary event
curl -X POST http://localhost:8000/apiaries/1/events \
  -H "Content-Type: application/json" \
  -d '{
    "description": "Annual inspection by local authority - passed"
  }'
```

### 6. Query Data
```bash
# Get all apiaries for a user
curl http://localhost:8000/apiaries?user_id=1

# Get all hives in an apiary
curl http://localhost:8000/hives?apiary_id=1

# Get queen history for a hive
curl http://localhost:8000/hives/1/queens

# Get hive events (newest first)
curl http://localhost:8000/hives/1/events

# Get telemetry
curl http://localhost:8000/hives/1/telemetry?limit=100
```

## Project Structure

```
backend/
├── main.py                 # FastAPI app entry point
├── requirements.txt        # Python dependencies
├── API_V2.md              # API documentation
├── models/
│   ├── __init__.py
│   ├── user_models.py     # User-related models
│   └── bee_models.py      # Apiary, Hive, Queen, Event models
└── controllers/
    ├── __init__.py
    ├── user_controller.py  # User CRUD endpoints
    └── bee_controller.py   # Bee management endpoints
```

## API Endpoint Summary

### Users
- `POST /users` - Create user
- `GET /users` - List all users
- `GET /users/{id}` - Get user
- `PUT /users/{id}` - Update user
- `DELETE /users/{id}` - Delete user

### Apiaries
- `POST /apiaries` - Create apiary
- `GET /apiaries?user_id={id}` - List apiaries
- `GET /apiaries/{id}` - Get apiary
- `PUT /apiaries/{id}` - Update apiary
- `DELETE /apiaries/{id}` - Delete apiary

### Hives
- `POST /hives` - Create hive
- `GET /hives?apiary_id={id}` - List hives
- `GET /hives/{id}` - Get hive
- `PUT /hives/{id}` - Update hive
- `DELETE /hives/{id}` - Delete hive

### Queen Bees
- `POST /hives/{id}/queens` - Introduce queen
- `GET /hives/{id}/queens` - List queens
- `GET /queens/{id}` - Get queen
- `PUT /queens/{id}` - Update queen
- `DELETE /queens/{id}` - Delete queen

### Events
- `POST /hives/{id}/events` - Create hive event
- `GET /hives/{id}/events` - Get hive events
- `POST /apiaries/{id}/events` - Create apiary event
- `GET /apiaries/{id}/events` - Get apiary events
- `DELETE /events/{id}` - Delete event

### Telemetry
- `GET /hives/{id}/telemetry` - Get telemetry data
- `WS /ws/hive/{id}/telemetry` - Real-time telemetry stream

## Testing

Use the interactive documentation at http://localhost:8000/docs to test all endpoints.

## Next Steps

1. **Authentication**: Implement JWT-based authentication
2. **Authorization**: Add user-level permissions (users can only access their own data)
3. **Password Hashing**: Use bcrypt or argon2 for secure password storage
4. **Validation**: Add more business logic validation
5. **WebSocket Authentication**: Secure WebSocket connections
6. **Rate Limiting**: Add rate limiting for API endpoints
7. **Testing**: Write unit and integration tests
8. **Frontend**: Update the web frontend to use the new API structure

## Troubleshooting

### Database Connection Issues
If you get database connection errors:
1. Make sure both databases are running: `docker-compose ps`
2. Check the database URLs in `main.py` or set environment variables:
   - `POSTGRES_URL=postgresql://beeapi:beeapi123@localhost:5432/beeapi`
   - `TIMESCALE_URL=postgresql://beeapi:beeapi123@localhost:5433/beeapi_telemetry`
3. Verify both databases are initialized:
   ```bash
   docker-compose logs postgres
   docker-compose logs timescaledb
   ```
4. Test connections:
   ```bash
   # PostgreSQL
   docker-compose exec postgres psql -U beeapi -d beeapi -c "\dt"
   
   # TimescaleDB
   docker-compose exec timescaledb psql -U beeapi -d beeapi_telemetry -c "\dt"
   ```

### Import Errors
If you get import errors:
1. Make sure you're in the `backend` directory when running
2. Check that all `__init__.py` files exist
3. Verify Python version is 3.8+

### Foreign Key Constraint Errors
If you get foreign key errors:
1. Ensure parent records exist before creating child records
2. Check that IDs are correct in your requests
3. Remember the hierarchy: User → Apiary → Hive → Queen
