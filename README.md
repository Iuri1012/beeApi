# BeeAPI - Beehive Monitoring System

A comprehensive IoT monitoring system for beehives with real-time telemetry, device management, and time-series data analytics.

## Architecture

This is a monorepo containing all components of the beehive monitoring system:

- **firmware/** - Device firmware and simulator for MQTT telemetry
- **gateway/** - IoT gateway services
- **backend/** - FastAPI REST API server
- **telemetry/** - MQTT telemetry consumer service
- **timeseries/** - TimescaleDB schema and migrations
- **web/** - React web dashboard
- **docs/** - Documentation
- **docker/** - Docker configurations
- **scripts/** - Utility scripts

## Tech Stack

- **MQTT**: Mosquitto for device communication
- **Database**: PostgreSQL with TimescaleDB extension
- **Backend**: FastAPI (Python)
- **Frontend**: Create React App
- **Containerization**: Docker & Docker Compose

## Quick Start

Run the entire system locally:

```bash
./scripts/run_local.sh
```

This will:
1. Start all services (MQTT, Database, Backend, Telemetry Consumer, Web UI)
2. Run the firmware simulator
3. Display live telemetry on the web dashboard at http://localhost:3000

## Development

### Prerequisites

- Docker and Docker Compose
- Python 3.9+ 
- Node.js 16+
- **Poetry** (recomendado para Python) - `brew install poetry`

### Package Management

O projeto usa Poetry para gerenciamento de dependências Python:

**Backend:**
```bash
cd backend
poetry install && poetry shell
python main.py
```

**Telemetry Consumer:**
```bash
cd telemetry  
poetry install && poetry shell
python consumer.py
```

**Firmware Simulator:**
```bash
cd firmware
poetry install && poetry shell  
python simulator.py --device-id hive-001
```

Ou use os scripts de desenvolvimento:
```bash
./scripts/dev.sh backend    # Inicia backend
./scripts/dev.sh telemetry  # Inicia consumer
./scripts/dev.sh simulator  # Inicia firmware
```

### 📖 Guias de Desenvolvimento

- **[📚 Central de Documentação](docs/README.md)** - Índice completo e organizado
- **[🚀 Quick Start](docs/guides/QUICKSTART.md)** - Setup em 5 minutos
- **[🔥 Backend Docs](backend/docs/README.md)** - Documentação completa do backend
- **[🏗️ Arquitetura](docs/architecture/DATABASE_ARCHITECTURE.md)** - Estrutura dos bancos

### Running Individual Services

See service-specific READMEs in each directory.

## API Endpoints

- `POST /register-device` - Register a new beehive device
- `GET /hives` - List all registered hives
- `WS /ws/hive/{id}/telemetry` - WebSocket for live telemetry

## License

MIT License - see LICENSE file for details.