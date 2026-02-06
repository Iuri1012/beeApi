# BeeAPI v2.0 - Database Architecture

## Overview

BeeAPI v2.0 uses a **dual-database architecture** to optimize performance by separating relational data from time-series data.

## Architecture Diagram

```
┌─────────────────────────────────────────┐
│         BeeAPI Backend (FastAPI)         │
│                                          │
│  ┌────────────────┐  ┌────────────────┐ │
│  │ User Controller│  │ Bee Controller │ │
│  │   (pg_pool)    │  │ (pg_pool +     │ │
│  │                │  │  ts_pool)      │ │
│  └────────┬───────┘  └───────┬────────┘ │
└───────────┼──────────────────┼──────────┘
            │                  │
            │                  └──────────┐
            │                             │
            ▼                             ▼
┌───────────────────────┐     ┌───────────────────────┐
│   PostgreSQL:5432     │     │  TimescaleDB:5433     │
│   Database: beeapi    │     │  Database:            │
│                       │     │  beeapi_telemetry     │
│  ┌─────────────────┐ │     │                       │
│  │ users           │ │     │  ┌─────────────────┐  │
│  │ apiaries        │ │     │  │ readings        │  │
│  │ hives           │ │     │  │ (hypertable)    │  │
│  │ queen_bees      │ │     │  └─────────────────┘  │
│  │ events          │ │     │  ┌─────────────────┐  │
│  └─────────────────┘ │     │  │ readings_hourly │  │
│                       │     │  │ (aggregate)     │  │
└───────────────────────┘     │  └─────────────────┘  │
                              └───────────────────────┘
```

## Database Separation

### PostgreSQL (Port 5432)
**Purpose:** Stores all relational/entity data

**Tables:**
- `users` - User accounts and authentication
- `apiaries` - Apiaries owned by users
- `hives` - Hives within apiaries
- `queen_bees` - Queen bee tracking (current and historical)
- `events` - Event logs for both hives and apiaries

**Characteristics:**
- Traditional relational database
- Full ACID compliance
- Foreign key constraints with CASCADE deletes
- Optimized for CRUD operations
- Supports complex joins and transactions

**Connection:**
- Default: `postgresql://beeapi:beeapi123@localhost:5432/beeapi`
- Environment variable: `POSTGRES_URL`
- Pool variable: `pg_pool`

### TimescaleDB (Port 5433)
**Purpose:** Stores only time-series telemetry data

**Tables:**
- `readings` - Sensor data (temperature, humidity, weight, sound_level)
  - **Hypertable** - automatically partitioned by time
- `readings_hourly` - Continuous aggregate for hourly statistics

**Characteristics:**
- PostgreSQL extension optimized for time-series
- Automatic data partitioning by time
- Continuous aggregates for fast queries
- Compression for old data
- Retention policies support
- Optimized for INSERT and time-range queries

**Connection:**
- Default: `postgresql://beeapi:beeapi123@localhost:5433/beeapi_telemetry`
- Environment variable: `TIMESCALE_URL`
- Pool variable: `ts_pool`

## Controller Usage

### User Controller
```python
# Uses ONLY PostgreSQL
db_pool = None  # PostgreSQL pool

def set_db_pool(pool):
    global db_pool
    db_pool = pool

# All operations use pg_pool for users table
async with db_pool.acquire() as conn:
    # User CRUD operations
```

### Bee Controller
```python
# Uses BOTH databases
pg_pool = None  # PostgreSQL for entities
ts_pool = None  # TimescaleDB for telemetry

def set_db_pools(postgres_pool, timescale_pool):
    global pg_pool, ts_pool
    pg_pool = postgres_pool
    ts_pool = timescale_pool

# Entity operations use pg_pool
async with pg_pool.acquire() as conn:
    # Apiaries, hives, queens, events

# Telemetry operations use ts_pool
async with ts_pool.acquire() as conn:
    # Readings queries
```

## Data Flow Examples

### 1. Create Hive
```
Client → POST /hives
    ↓
Bee Controller
    ↓
pg_pool → PostgreSQL
    ↓
INSERT INTO hives (device_id, name, apiary_id)
```

### 2. Get Telemetry
```
Client → GET /hives/1/telemetry
    ↓
Bee Controller
    ↓
pg_pool → PostgreSQL: SELECT device_id FROM hives WHERE id=1
    ↓
ts_pool → TimescaleDB: SELECT * FROM readings WHERE device_id='hive-001'
    ↓
Return telemetry data
```

### 3. WebSocket Telemetry Stream
```
Client → WS /ws/hive/1/telemetry
    ↓
Bee Controller
    ↓
pg_pool → PostgreSQL: Verify hive exists, get device_id
    ↓
ts_pool → TimescaleDB: Get last 10 readings
    ↓
Stream real-time updates
```

## Benefits of This Architecture

### 1. Performance
- **PostgreSQL** handles complex joins efficiently
- **TimescaleDB** handles millions of time-series records efficiently
- Each database is optimized for its specific workload

### 2. Scalability
- Can scale each database independently
- TimescaleDB can handle high INSERT rates without affecting user queries
- Continuous aggregates pre-compute common queries

### 3. Data Management
- **TimescaleDB features:**
  - Automatic data compression for old readings
  - Retention policies to drop old data
  - Time-based partitioning

### 4. Separation of Concerns
- Business logic data (users, apiaries) separate from sensor data
- Easier to backup and restore
- Can apply different security policies

## Configuration

### Docker Compose
```yaml
services:
  postgres:
    image: postgres:15
    ports: ["5432:5432"]
    environment:
      POSTGRES_DB: beeapi
      POSTGRES_USER: beeapi
      POSTGRES_PASSWORD: beeapi123
    volumes:
      - ./postgres/init.sql:/docker-entrypoint-initdb.d/init.sql

  timescaledb:
    image: timescale/timescaledb:latest-pg15
    ports: ["5433:5432"]  # Note: 5433 on host
    environment:
      POSTGRES_DB: beeapi_telemetry
      POSTGRES_USER: beeapi
      POSTGRES_PASSWORD: beeapi123
    volumes:
      - ./timeseries/init.sql:/docker-entrypoint-initdb.d/init.sql
```

### Application Startup
```python
@app.on_event("startup")
async def startup():
    global pg_pool, ts_pool
    
    # PostgreSQL connection
    pg_url = os.getenv("POSTGRES_URL", 
        "postgresql://beeapi:beeapi123@localhost:5432/beeapi")
    pg_pool = await asyncpg.create_pool(pg_url, min_size=2, max_size=10)
    
    # TimescaleDB connection
    ts_url = os.getenv("TIMESCALE_URL",
        "postgresql://beeapi:beeapi123@localhost:5433/beeapi_telemetry")
    ts_pool = await asyncpg.create_pool(ts_url, min_size=2, max_size=10)
    
    # Distribute pools to controllers
    user_controller.set_db_pool(pg_pool)
    bee_controller.set_db_pools(pg_pool, ts_pool)
```

## Cross-Database References

### Device ID Linking
The `readings` table in TimescaleDB references `device_id` from the `hives` table in PostgreSQL:

```
PostgreSQL:  hives.device_id (unique)
                    ↕
TimescaleDB: readings.device_id
```

**Note:** We don't enforce foreign key constraints across databases. The application layer ensures referential integrity by:
1. Checking hive exists before querying telemetry
2. Using device_id as the linking field
3. Application-level validation

### Data Cleanup
When a hive is deleted:
1. PostgreSQL CASCADE deletes related queens and events
2. Telemetry data in TimescaleDB remains (historical record)
3. Can be cleaned up manually or with retention policies

## Query Patterns

### Simple Entity Queries
Use PostgreSQL directly:
```sql
-- Get user's apiaries
SELECT * FROM apiaries WHERE user_id = $1;

-- Get apiary's hives
SELECT * FROM hives WHERE apiary_id = $1;
```

### Time-Series Queries
Use TimescaleDB for efficiency:
```sql
-- Recent readings
SELECT * FROM readings 
WHERE device_id = $1 
  AND time > NOW() - INTERVAL '24 hours'
ORDER BY time DESC;

-- Hourly averages (uses continuous aggregate)
SELECT * FROM readings_hourly
WHERE device_id = $1
  AND bucket > NOW() - INTERVAL '7 days'
ORDER BY bucket DESC;
```

### Combined Queries
Query both databases when needed:
```python
# Get hive info from PostgreSQL
hive = await pg_pool.fetchrow("SELECT * FROM hives WHERE id = $1", hive_id)

# Get telemetry from TimescaleDB
readings = await ts_pool.fetch(
    "SELECT * FROM readings WHERE device_id = $1 LIMIT 100",
    hive['device_id']
)
```

## Migration Notes

### From Single Database
If migrating from a single-database setup:

1. **Export entity data:**
   ```bash
   pg_dump -t users -t apiaries -t hives -t queen_bees -t events beeapi > entities.sql
   ```

2. **Export telemetry data:**
   ```bash
   pg_dump -t readings beeapi > telemetry.sql
   ```

3. **Import to respective databases:**
   ```bash
   psql -h localhost -p 5432 -U beeapi -d beeapi < entities.sql
   psql -h localhost -p 5433 -U beeapi -d beeapi_telemetry < telemetry.sql
   ```

## Monitoring

### Check Database Status
```bash
# PostgreSQL
docker-compose exec postgres psql -U beeapi -d beeapi -c "\dt"

# TimescaleDB
docker-compose exec timescaledb psql -U beeapi -d beeapi_telemetry -c "\dx"
```

### Check Data Sizes
```bash
# PostgreSQL tables
docker-compose exec postgres psql -U beeapi -d beeapi -c "
SELECT schemaname, tablename, pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename))
FROM pg_tables WHERE schemaname = 'public';"

# TimescaleDB hypertable
docker-compose exec timescaledb psql -U beeapi -d beeapi_telemetry -c "
SELECT hypertable_size('readings');"
```

## Best Practices

1. **Connection Pooling:** Both databases use connection pools (min=2, max=10)
2. **Error Handling:** Catch database errors separately for each connection
3. **Transactions:** Keep transactions short and database-specific
4. **Indexes:** Maintained automatically by init scripts
5. **Backups:** Back up both databases separately
6. **Monitoring:** Monitor both database connections and performance

## Future Enhancements

Potential improvements to the architecture:

1. **Read Replicas:** Add read replicas for high-traffic queries
2. **Sharding:** Shard TimescaleDB by device_id for extreme scale
3. **Caching:** Add Redis for frequently accessed entity data
4. **Data Warehousing:** Export aggregated data to analytics database
5. **Compression:** Enable TimescaleDB compression for old data
6. **Retention Policies:** Automatically drop telemetry older than X months
