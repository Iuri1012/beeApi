# Firmware Simulator

> Simulates beehive IoT devices that publish telemetry data via MQTT

## 🚀 Installation

```bash
poetry install              # Install dependencies
poetry shell               # Activate environment
python simulator.py --device-id hive-001  # Run simulator
```

## 📖 Poetry Commands

```bash
# Setup
poetry install              # Install dependencies
poetry env info            # View environment info

# Running
poetry shell               # Activate environment
python simulator.py --device-id hive-001  # Run simulator
# or
poetry run python simulator.py --device-id hive-001  # Run without activating

# Development
poetry add package         # Add dependency
poetry show               # List installed packages
```

## 💻 Usage

### Basic Usage
```bash
poetry run python simulator.py --device-id hive-001 --broker localhost --interval 5
```

Options:
- `--device-id`: Unique device identifier (default: hive-001)
- `--broker`: MQTT broker hostname (default: localhost)
- `--port`: MQTT broker port (default: 1883)
- `--interval`: Seconds between telemetry transmissions (default: 5)
- `--count`: Number of messages to send (default: infinite)

## Telemetry Format

```json
{
  "device_id": "hive-001",
  "timestamp": "2026-02-03T13:00:00Z",
  "temperature": 35.5,
  "humidity": 62.3,
  "weight": 45.2,
  "sound_level": 48.7
}
```
