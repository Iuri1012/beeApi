# End-to-End Testing Guide

This guide walks through testing the complete BeeAPI system from device simulation to web dashboard.

## Prerequisites

- Docker and Docker Compose v2
- Python 3.9+
- Node.js 16+ (optional, for local web development)

## Quick Test (Without Docker)

To validate the structure and component logic without running the full stack:

```bash
# Validate repository structure
./scripts/validate_structure.sh

# Run integration tests
python3 scripts/test_integration.py
```

## Full Stack Test (With Docker)

### 1. Start All Services

```bash
./scripts/run_local.sh
```

This script will:
1. Start Docker services (Mosquitto, PostgreSQL, Backend, Telemetry Consumer, Web)
2. Wait for services to be ready
3. Launch the firmware simulator

### 2. Verify Services

Once running, verify each component:

#### MQTT Broker
```bash
# Subscribe to telemetry topic
mosquitto_sub -h localhost -t "beehive/+/telemetry"
```

#### Database
```bash
# Connect to database
docker compose exec postgres psql -U beeapi -d beeapi

# Query hives
SELECT * FROM hives;

# Query recent readings
SELECT * FROM readings ORDER BY time DESC LIMIT 10;
```

#### Backend API
```bash
# Health check
curl http://localhost:8000/

# List hives
curl http://localhost:8000/hives

# Get telemetry
curl http://localhost:8000/hives/hive-001/telemetry?limit=10
```

#### Web Dashboard
Open browser to: http://localhost:3000

You should see:
- Live telemetry metrics (temperature, humidity, weight, sound level)
- Real-time charts updating as simulator publishes data
- "Live" indicator showing WebSocket connection

### 3. Test Data Flow

Monitor the complete data flow:

```bash
# Terminal 1: Watch MQTT messages
docker compose logs -f mosquitto

# Terminal 2: Watch telemetry consumer
docker compose logs -f telemetry

# Terminal 3: Watch backend
docker compose logs -f backend

# Terminal 4: Watch database inserts
docker compose exec postgres psql -U beeapi -d beeapi -c "SELECT COUNT(*) FROM readings;"
# Run this command multiple times to see count increasing
```

### 4. Register Additional Devices

```bash
# Register a new device
curl -X POST http://localhost:8000/register-device \
  -H "Content-Type: application/json" \
  -d '{
    "device_id": "hive-002",
    "name": "Hive Beta",
    "location": "Apiary B"
  }'

# Run a second simulator for the new device
cd firmware
source venv/bin/activate
python simulator.py --device-id hive-002 --interval 5
```

The web dashboard will automatically show the new hive.

### 5. Test WebSocket

```bash
# Using websocat (install with: cargo install websocat)
websocat ws://localhost:8000/ws/hive/hive-001/telemetry
```

You should see real-time telemetry messages streaming.

## Stopping Services

```bash
docker compose down

# To remove volumes as well (cleans database)
docker compose down -v
```

## Troubleshooting

### Services won't start
```bash
# Check logs
docker compose logs

# Restart specific service
docker compose restart backend
```

### Database connection issues
```bash
# Check postgres is ready
docker compose exec postgres pg_isready -U beeapi

# Check database exists
docker compose exec postgres psql -U beeapi -l
```

### Web not loading
```bash
# Web takes longest to start (npm install on first run)
# Check logs
docker compose logs web

# May take 2-3 minutes on first run
```

### MQTT issues
```bash
# Test MQTT directly
docker compose exec mosquitto mosquitto_sub -t "beehive/+/telemetry"
```

## Performance Testing

### High-Volume Simulation

Run multiple simulators to test under load:

```bash
# Terminal 1
python firmware/simulator.py --device-id hive-001 --interval 1

# Terminal 2
python firmware/simulator.py --device-id hive-002 --interval 1

# Terminal 3
python firmware/simulator.py --device-id hive-003 --interval 1
```

Monitor system resources:
```bash
docker stats
```

### Database Performance

Check query performance:
```bash
docker compose exec postgres psql -U beeapi -d beeapi

-- Explain query plan
EXPLAIN ANALYZE SELECT * FROM readings WHERE device_id = 'hive-001' ORDER BY time DESC LIMIT 100;

-- Check hypertable chunks
SELECT * FROM timescaledb_information.chunks WHERE hypertable_name = 'readings';

-- Check continuous aggregate
SELECT * FROM readings_hourly ORDER BY bucket DESC LIMIT 10;
```

## Acceptance Criteria

✅ All services start successfully  
✅ Simulator publishes MQTT messages  
✅ Telemetry consumer stores data in database  
✅ Backend API responds to requests  
✅ Web dashboard displays live telemetry  
✅ WebSocket connection shows "Live" status  
✅ Charts update in real-time  
✅ Multiple hives can be monitored simultaneously  

## Next Steps

For production deployment:
- Add authentication/authorization
- Configure TLS/SSL for MQTT and API
- Set up data retention policies
- Add monitoring and alerting
- Implement rate limiting
- Add comprehensive test suite
