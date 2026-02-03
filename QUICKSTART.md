# BeeAPI - Quick Start Guide

Get your beehive monitoring system running in 5 minutes!

## Prerequisites

- Docker and Docker Compose v2 installed
- 4GB RAM minimum
- Ports 1883, 3000, 5432, 8000 available

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Iuri1012/beeApi.git
cd beeApi
```

### 2. Start the System

```bash
./scripts/run_local.sh
```

This single command will:
- Start all Docker services (MQTT, Database, Backend, Telemetry, Web)
- Initialize the database with schema
- Run the beehive simulator
- Open the web dashboard

### 3. View the Dashboard

Open your browser to: **http://localhost:3000**

You should see:
- 🐝 Live telemetry from "hive-001"
- 🌡️ Temperature, humidity, weight, sound metrics
- 📊 Real-time updating charts
- ✅ "Live" connection indicator

## What You're Seeing

The simulator is publishing realistic beehive sensor data every 5 seconds:
- **Temperature**: 33-37°C (hive internal temperature)
- **Humidity**: 55-65% (hive moisture levels)
- **Weight**: 44-46 kg (hive + honey weight)
- **Sound Level**: 40-60 dB (colony activity)

This data flows through:
1. Simulator → MQTT broker
2. MQTT → Telemetry consumer
3. Consumer → TimescaleDB
4. Database → Backend API
5. API → Web dashboard (via WebSocket)

## Exploring the System

### View API Documentation
http://localhost:8000/docs

### Register a New Device

```bash
curl -X POST http://localhost:8000/register-device \
  -H "Content-Type: application/json" \
  -d '{
    "device_id": "hive-002",
    "name": "Alpha Hive",
    "location": "Apiary Garden"
  }'
```

### Query Telemetry via API

```bash
# List all hives
curl http://localhost:8000/hives

# Get telemetry history
curl http://localhost:8000/hives/hive-001/telemetry?limit=10
```

### Access the Database

```bash
docker compose exec postgres psql -U beeapi -d beeapi
```

Example queries:
```sql
-- View all hives
SELECT * FROM hives;

-- Recent telemetry
SELECT * FROM readings ORDER BY time DESC LIMIT 10;

-- Hourly averages
SELECT * FROM readings_hourly ORDER BY bucket DESC LIMIT 24;
```

### Monitor Services

```bash
# View all service logs
docker compose logs -f

# View specific service
docker compose logs -f backend
docker compose logs -f telemetry

# Check service status
docker compose ps
```

## Adding More Simulators

Run additional simulators for multiple hives:

```bash
# Terminal 1 - First simulator
cd firmware
python3 simulator.py --device-id hive-001 --interval 5

# Terminal 2 - Second simulator  
cd firmware
python3 simulator.py --device-id hive-002 --interval 5

# Terminal 3 - Third simulator
cd firmware
python3 simulator.py --device-id hive-003 --interval 5
```

The dashboard will automatically show all active hives!

## Stopping the System

```bash
# Stop all services
docker compose down

# Stop and remove data (clean slate)
docker compose down -v
```

## Troubleshooting

### Services won't start

```bash
# Check Docker is running
docker info

# Check port availability
netstat -tuln | grep -E "1883|3000|5432|8000"

# View error logs
docker compose logs
```

### Database issues

```bash
# Restart database
docker compose restart postgres

# Check database health
docker compose exec postgres pg_isready -U beeapi
```

### Web dashboard not loading

```bash
# Web takes 2-3 minutes on first run (npm install)
# Check logs
docker compose logs web

# Restart web service
docker compose restart web
```

### MQTT connection issues

```bash
# Test MQTT directly
docker compose exec mosquitto mosquitto_pub -t "test" -m "hello"
docker compose exec mosquitto mosquitto_sub -t "test"
```

## Next Steps

- **Read the docs**: Check `docs/` directory for detailed documentation
- **Explore the API**: Visit http://localhost:8000/docs
- **Customize**: Modify services in their respective directories
- **Deploy**: See `docs/TESTING.md` for production deployment

## Getting Help

- **Documentation**: See `docs/` directory
- **Issues**: https://github.com/Iuri1012/beeApi/issues
- **Contributing**: See `CONTRIBUTING.md`

## What's in the Box

```
beeApi/
├── firmware/      - Device simulator
├── backend/       - REST API
├── telemetry/     - MQTT consumer
├── timeseries/    - Database schema
├── web/           - React dashboard
├── docs/          - Documentation
└── scripts/       - Utilities
```

Enjoy your beehive monitoring system! 🐝
