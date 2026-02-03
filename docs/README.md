# Documentation

## Architecture Overview

The BeeAPI system consists of several components:

```
┌─────────────┐
│  Beehive    │
│  Devices    │──MQTT──┐
└─────────────┘        │
                       ▼
┌─────────────┐   ┌──────────┐   ┌─────────────┐
│  Firmware   │   │ Mosquitto│   │ Telemetry   │
│  Simulator  │──▶│  (MQTT)  │──▶│  Consumer   │
└─────────────┘   └──────────┘   └──────┬──────┘
                                         │
                                         ▼
                  ┌─────────────────────────┐
                  │   PostgreSQL +          │
                  │   TimescaleDB           │
                  └───────────┬─────────────┘
                              │
                              ▼
┌─────────────┐   ┌──────────────────┐
│   React     │   │  FastAPI         │
│   Web UI    │◀──│  Backend         │
└─────────────┘   └──────────────────┘
```

## Data Flow

1. **Device → MQTT**: Beehive devices publish telemetry to MQTT topics
2. **MQTT → Consumer**: Telemetry consumer subscribes and receives messages
3. **Consumer → Database**: Consumer stores data in TimescaleDB hypertable
4. **Web → Backend**: React app fetches data via REST API
5. **Backend → Web**: WebSocket streams real-time updates

## Components

### Firmware Simulator
- Simulates beehive IoT devices
- Publishes realistic telemetry data
- Configurable interval and device ID

### MQTT Broker (Mosquitto)
- Message broker for device communication
- Topic structure: `beehive/{device_id}/telemetry`

### Telemetry Consumer
- Python service subscribing to MQTT
- Validates and stores data in database
- Handles device registration checks

### Backend API (FastAPI)
- RESTful API for device and data management
- WebSocket support for real-time updates
- Async database connections

### TimescaleDB
- Time-series database for telemetry
- Hypertable for efficient time-based queries
- Continuous aggregates for analytics

### Web Dashboard
- React-based UI
- Real-time charts and metrics
- WebSocket integration for live data

## API Reference

See [API.md](API.md) for detailed endpoint documentation.

## Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for production deployment guide.
