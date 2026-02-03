# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-02-03

### Added

#### Core Infrastructure
- Monorepo structure with firmware, gateway, backend, telemetry, timeseries, web, docs, docker directories
- Docker Compose configuration for full stack deployment
- MIT License
- Comprehensive .gitignore
- README with quick start guide

#### Firmware
- Python-based beehive simulator (`firmware/simulator.py`)
- MQTT telemetry publishing
- Configurable device ID, broker, interval
- Realistic sensor data generation (temperature, humidity, weight, sound level)

#### Database (TimescaleDB)
- PostgreSQL with TimescaleDB extension
- Hives table for device registration
- Readings hypertable for time-series telemetry
- Indexes for optimized queries
- Continuous aggregate for hourly statistics
- Sample data initialization

#### Backend (FastAPI)
- REST API with OpenAPI documentation
- `POST /register-device` - Device registration
- `GET /hives` - List all hives
- `GET /hives/{device_id}` - Get specific hive
- `GET /hives/{device_id}/telemetry` - Historical telemetry
- `WS /ws/hive/{device_id}/telemetry` - Real-time WebSocket
- CORS middleware for web integration
- AsyncPG for database connections
- WebSocket connection manager

#### Telemetry Consumer
- MQTT subscriber for beehive telemetry
- Automatic data validation and storage
- Device registration verification
- Error handling and logging
- TimescaleDB integration

#### Web Dashboard (React)
- Create React App setup
- Real-time telemetry visualization
- WebSocket integration for live updates
- Recharts for data visualization
- Responsive design
- Multi-hive support
- Metrics cards (temperature, humidity, weight, sound)
- Time-series charts
- Connection status indicator

#### Documentation
- API documentation (`docs/API.md`)
- Architecture overview (`docs/README.md`)
- Testing guide (`docs/TESTING.md`)
- Contributing guidelines (`CONTRIBUTING.md`)

#### GitHub Templates
- Bug report template
- Feature request template
- Pull request template

#### CI/CD
- GitHub Actions workflow
- Backend linting (Black, Flake8)
- Web build validation
- Docker smoke tests
- API endpoint testing

#### Scripts
- `scripts/run_local.sh` - One-command local deployment
- `scripts/dev.sh` - Local development helper
- `scripts/validate_structure.sh` - Repository structure validation
- `scripts/test_integration.py` - Integration test suite

#### Docker
- Mosquitto MQTT broker configuration
- Backend Dockerfile with FastAPI
- Telemetry consumer Dockerfile
- Web Dockerfile with CRA
- TimescaleDB initialization
- Multi-service orchestration
- Health checks and dependencies

### Technical Details

**Backend Stack:**
- Python 3.11
- FastAPI 0.109.0
- AsyncPG 0.29.0
- Pydantic 2.5.3
- Uvicorn

**Frontend Stack:**
- React 18.2.0
- Recharts 2.10.3
- Axios 1.6.5

**Infrastructure:**
- Mosquitto 2
- TimescaleDB (PostgreSQL 15)
- Docker Compose v2

**Protocols:**
- MQTT for device communication
- HTTP/REST for API
- WebSocket for real-time updates

### Acceptance Criteria Met

✅ Monorepo structure with all required folders  
✅ README, LICENSE (MIT), .gitignore  
✅ Docker Compose with Mosquitto, Postgres+Timescale, FastAPI, telemetry consumer, web  
✅ firmware/simulator.py publishes MQTT  
✅ timeseries SQL with readings hypertable  
✅ Backend endpoints: /register-device, /hives, /ws/hive/{id}/telemetry  
✅ GitHub templates (issues, PRs)  
✅ CI workflow (lint, tests, docker smoke)  
✅ scripts/run_local.sh  
✅ End-to-end flow: run_local.sh + simulator → web shows live telemetry

[1.0.0]: https://github.com/Iuri1012/beeApi/releases/tag/v1.0.0
