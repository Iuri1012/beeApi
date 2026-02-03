# Firmware Simulator

Simulates beehive IoT devices that publish telemetry data via MQTT.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python simulator.py --device-id hive-001 --broker localhost --interval 5
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
