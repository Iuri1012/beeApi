# TimescaleDB Schema

This directory contains database schemas and migrations for the BeeAPI system.

## Schema

The database uses PostgreSQL with the TimescaleDB extension for time-series data.

### Tables

#### hives
Stores registered beehive devices.

| Column | Type | Description |
|--------|------|-------------|
| id | SERIAL | Primary key |
| device_id | VARCHAR(255) | Unique device identifier |
| name | VARCHAR(255) | Display name |
| location | VARCHAR(255) | Physical location |
| registered_at | TIMESTAMP | Registration timestamp |

#### readings (Hypertable)
Stores telemetry readings with time-series optimization.

| Column | Type | Description |
|--------|------|-------------|
| time | TIMESTAMPTZ | Timestamp (partition key) |
| device_id | VARCHAR(255) | Device identifier |
| temperature | DOUBLE PRECISION | Temperature in Celsius |
| humidity | DOUBLE PRECISION | Humidity percentage |
| weight | DOUBLE PRECISION | Weight in kilograms |
| sound_level | DOUBLE PRECISION | Sound level in decibels |

### Continuous Aggregates

#### readings_hourly
Pre-computed hourly aggregates for faster queries.

- Average values per hour
- Min/Max temperature
- Grouped by device_id

## Initialization

The `init.sql` file is automatically executed when the PostgreSQL container starts for the first time.

## Manual Queries

Connect to the database:
```bash
docker-compose exec postgres psql -U beeapi -d beeapi
```

Example queries:
```sql
-- Get latest readings
SELECT * FROM readings ORDER BY time DESC LIMIT 10;

-- Get hourly averages
SELECT * FROM readings_hourly ORDER BY bucket DESC LIMIT 24;

-- Get readings for specific device
SELECT * FROM readings WHERE device_id = 'hive-001' ORDER BY time DESC;
```

## Data Retention

Currently, data is kept indefinitely. For production, consider adding retention policies:

```sql
SELECT add_retention_policy('readings', INTERVAL '90 days');
```
