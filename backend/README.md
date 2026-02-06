# Backend API

> FastAPI-based REST API for beehive monitoring with Poetry dependency management

## 🚀 Quick Start

```bash
poetry install              # Install dependencies
poetry shell               # Activate environment  
python main.py             # Start server
```

## 📖 Documentation

📚 **[Complete Documentation](docs/README.md)** - Full backend docs index

### Quick Links
- **[Poetry Guide](docs/POETRY_GUIDE.md)** - Learn Poetry
- **[Poetry Cheat Sheet](docs/POETRY_CHEATSHEET.md)** - Daily commands
- **[API Documentation](docs/API_V2.md)** - All endpoints
- **[Migration Guide](docs/MIGRATION_GUIDE.md)** - Database setup
- **[Firebase Setup](docs/FIREBASE_SETUP.md)** - Authentication config

## 🔗 API Access

- **Server**: http://localhost:8000
- **Swagger UI**: http://localhost:8000/docs
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## ⚡ Key Endpoints

- `POST /register-device` - Register a new device
- `GET /hives` - List all hives
- `GET /hives/{device_id}` - Get specific hive
- `GET /hives/{device_id}/telemetry` - Get telemetry history
- `WS /ws/hive/{device_id}/telemetry` - Real-time telemetry WebSocket
