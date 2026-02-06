# Telemetry Consumer

> MQTT consumer that subscribes to beehive telemetry and stores it in TimescaleDB

## 🚀 Installation

```bash
poetry install              # Install dependencies
poetry shell               # Activate environment
python consumer.py         # Run consumer
```

## 📖 Poetry Commands

```bash
# Setup
poetry install              # Install dependencies
poetry env info            # View environment info

# Running
poetry shell               # Activate environment
python consumer.py         # Run consumer
# or
poetry run python consumer.py  # Run without activating

# Development
poetry add package         # Add dependency
poetry show               # List installed packages
```

## Environment Variables

- `MQTT_BROKER` - MQTT broker hostname (default: localhost)
- `MQTT_PORT` - MQTT broker port (default: 1883)
- `DATABASE_URL` - PostgreSQL connection string
