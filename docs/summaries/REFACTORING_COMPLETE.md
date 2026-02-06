# Database Refactoring Complete! 🎉

## What Changed

Successfully refactored BeeAPI v2.0 to use a **dual-database architecture** for optimal performance.

### Before (Single Database)
```
TimescaleDB (5432)
  ├── users
  ├── apiaries  
  ├── hives
  ├── queen_bees
  ├── events
  └── readings (hypertable)
```

### After (Dual Database) ✅
```
PostgreSQL (5432)              TimescaleDB (5433)
  ├── users                      └── readings (hypertable)
  ├── apiaries                   └── readings_hourly (aggregate)
  ├── hives
  ├── queen_bees
  └── events
```

## Why This Is Better

### PostgreSQL (Port 5432)
**Purpose:** Relational/entity data  
**Optimized for:**
- Complex joins and relationships
- CRUD operations
- Transaction management
- Business logic

### TimescaleDB (Port 5433)  
**Purpose:** Time-series telemetry data  
**Optimized for:**
- High-frequency sensor readings
- Time-based queries and aggregations
- Data compression
- Automatic partitioning

## Changes Made

### 1. Docker Compose
- ✅ Added separate `postgres` service (port 5432)
- ✅ Updated `timescaledb` service (port 5433)
- ✅ Added both database volumes
- ✅ Updated environment variables

### 2. Database Schemas
- ✅ Created `postgres/init.sql` - relational tables
- ✅ Updated `timeseries/init.sql` - ONLY readings

### 3. Backend Application
- ✅ Updated `main.py` - dual connection pools
- ✅ Updated `user_controller.py` - uses `pg_pool`
- ✅ Updated `bee_controller.py` - uses `pg_pool` + `ts_pool`
  - Entity operations → PostgreSQL
  - Telemetry queries → TimescaleDB

### 4. Documentation
- ✅ Updated `API_V2.md` - database architecture section
- ✅ Updated `MIGRATION_GUIDE.md` - dual database setup
- ✅ Updated `QUICK_REFERENCE.md`
- ✅ Updated `UPDATE_SUMMARY.md`
- ✅ Created `DATABASE_ARCHITECTURE.md` - comprehensive guide
- ✅ Created `.env.example` - configuration template

## How to Use

### 1. Start Services
```bash
# Start both databases
docker-compose up -d postgres timescaledb

# Verify both are running
docker-compose ps
```

### 2. Check Databases
```bash
# PostgreSQL tables
docker-compose exec postgres psql -U beeapi -d beeapi -c "\dt"

# Expected: users, apiaries, hives, queen_bees, events

# TimescaleDB tables
docker-compose exec timescaledb psql -U beeapi -d beeapi_telemetry -c "\dt"

# Expected: readings, readings_hourly
```

### 3. Run Application
```bash
cd backend
python main.py
```

You should see:
```
✓ PostgreSQL connection pool created: localhost:5432/beeapi
✓ TimescaleDB connection pool created: localhost:5433/beeapi_telemetry
✓ Database pools configured in controllers
```

### 4. Test API
```bash
cd backend
python test_api.py
```

## Environment Variables

Create a `.env` file (or use defaults):
```bash
# PostgreSQL (relational data)
POSTGRES_URL=postgresql://beeapi:beeapi123@localhost:5432/beeapi

# TimescaleDB (time-series data)
TIMESCALE_URL=postgresql://beeapi:beeapi123@localhost:5433/beeapi_telemetry
```

## Migration from Previous Version

If you have existing data in a single TimescaleDB:

```bash
# 1. Backup everything
docker-compose exec postgres pg_dump -U beeapi beeapi > backup.sql

# 2. Stop containers
docker-compose down -v

# 3. Start fresh with new architecture
docker-compose up -d postgres timescaledb

# 4. Restore to appropriate databases
# (Entity data to PostgreSQL, telemetry to TimescaleDB)
```

## Verification

### Check Connections
```bash
# Test PostgreSQL
curl http://localhost:8000/users

# Test TimescaleDB (via hive telemetry)
curl http://localhost:8000/hives/1/telemetry
```

### Database Sizes
```bash
# PostgreSQL
docker-compose exec postgres psql -U beeapi -d beeapi -c "
SELECT schemaname, tablename, pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename))
FROM pg_tables WHERE schemaname = 'public';"

# TimescaleDB
docker-compose exec timescaledb psql -U beeapi -d beeapi_telemetry -c "
SELECT pg_size_pretty(hypertable_size('readings'));"
```

## Benefits

✅ **Performance:** Each database optimized for its workload  
✅ **Scalability:** Scale relational and time-series data independently  
✅ **Flexibility:** Different backup/retention policies per database  
✅ **Clarity:** Clear separation of concerns  
✅ **TimescaleDB Features:** Compression, retention policies, continuous aggregates  

## Documentation

- **Quick Start:** `QUICK_REFERENCE.md`
- **Full API Docs:** `backend/API_V2.md`
- **Migration Guide:** `backend/MIGRATION_GUIDE.md`
- **Database Design:** `DATABASE_ARCHITECTURE.md`
- **Change Summary:** `UPDATE_SUMMARY.md`

## Next Steps

1. ✅ Databases properly separated
2. ✅ Code using appropriate pools
3. ✅ Documentation updated
4. ⏭️ Test with real telemetry data
5. ⏭️ Configure retention policies (optional)
6. ⏭️ Enable compression for old data (optional)

## Success! 🐝

The BeeAPI v2.0 now uses a professional, scalable dual-database architecture that properly leverages PostgreSQL for relational data and TimescaleDB for time-series telemetry.
