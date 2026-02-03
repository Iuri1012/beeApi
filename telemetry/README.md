# Telemetry Consumer

MQTT consumer that subscribes to beehive telemetry and stores it in TimescaleDB.

## Installation

```bash
pip install -r requirements.txt
```

## Running

```bash
python consumer.py
```

## Environment Variables

- `MQTT_BROKER` - MQTT broker hostname (default: localhost)
- `MQTT_PORT` - MQTT broker port (default: 1883)
- `DATABASE_URL` - PostgreSQL connection string
