# 🤖 Firmware Simulator - Poetry Guide

## 🚀 Quick Start with Poetry

```bash
# Clone and setup
git clone https://github.com/Iuri1012/beeApi.git
cd beeApi/firmware

# Install with Poetry
poetry install

# Run simulator
poetry shell
python simulator.py --device-id hive-001
```

## 📦 Dependencies

### Production
- **paho-mqtt 1.6.1** - MQTT client library for IoT communication

### Development
- **pytest** - Testing framework for device simulation tests

## 💻 Development Commands

```bash
# Environment management
poetry install              # Install all dependencies
poetry shell               # Activate virtual environment
poetry env info            # Show environment details

# Running simulator
poetry run python simulator.py --device-id hive-001 --broker localhost
poetry run python simulator.py --help    # Show all options

# Multiple devices simulation
poetry run python simulator.py --device-id hive-001 &
poetry run python simulator.py --device-id hive-002 &
poetry run python simulator.py --device-id hive-003 &

# Testing (when tests are added)
poetry run pytest          # Run tests
poetry add --group dev pytest-mock  # Add mocking support

# Dependency management
poetry add requests        # Add HTTP client (if needed)
poetry add --group dev black      # Add code formatter
poetry show                # List all packages
poetry update              # Update all dependencies
```

## 🎛️ Simulator Options

```bash
# Basic usage
poetry run python simulator.py \
  --device-id hive-001 \
  --broker localhost \
  --port 1883 \
  --interval 5 \
  --count 100

# Available parameters:
# --device-id    : Unique device identifier (default: hive-001)
# --broker       : MQTT broker hostname (default: localhost)  
# --port         : MQTT broker port (default: 1883)
# --interval     : Seconds between messages (default: 5)
# --count        : Number of messages to send (default: infinite)
```

## 🔧 Configuration

### Environment Variables
```bash
# Create .env file for simulator
DEVICE_ID=hive-001
MQTT_BROKER=localhost
MQTT_PORT=1883
TELEMETRY_INTERVAL=5
```

### Poetry Config
```bash
# Show current config
poetry config --list

# Set virtualenv in project (optional)
poetry config virtualenvs.in-project true

# Remove environment (if needed)
poetry env remove python
```

## 📡 MQTT Message Format

The simulator publishes telemetry in this format:
```json
{
  "device_id": "hive-001",
  "timestamp": "2026-02-06T13:00:00Z",
  "temperature": 35.5,
  "humidity": 65.2,
  "weight": 45.8
}
```

## 🐳 Docker Integration

### Dockerfile with Poetry
```dockerfile
FROM python:3.9-slim

# Install Poetry
RUN pip install poetry

# Copy Poetry files
COPY pyproject.toml poetry.lock ./

# Configure Poetry
RUN poetry config virtualenvs.create false

# Install dependencies
RUN poetry install --no-dev

# Copy source
COPY . .

# Run simulator
CMD ["poetry", "run", "python", "simulator.py", "--device-id", "hive-docker"]
```

### Docker Compose Service
```yaml
firmware-simulator:
  build: ./firmware
  environment:
    - DEVICE_ID=hive-docker
    - MQTT_BROKER=mosquitto
  depends_on:
    - mosquitto
```

## 🧪 Testing Setup

```bash
# Add testing dependencies
poetry add --group dev pytest pytest-mock

# Example test structure
mkdir tests
touch tests/test_simulator.py

# Run tests
poetry run pytest tests/
```

## 🔍 Troubleshooting

### Common Issues

1. **MQTT Connection Failed**
   ```bash
   # Check if broker is running
   docker-compose up -d mosquitto
   
   # Test connection
   poetry run python simulator.py --broker localhost --device-id test
   ```

2. **Python version issues**
   ```bash
   poetry env use python3.9
   poetry install
   ```

3. **Permission issues**
   ```bash
   poetry cache clear pypi --all
   poetry install
   ```

## 📊 Project Structure

```
firmware/
├── pyproject.toml          # Poetry configuration
├── poetry.lock            # Lock file
├── requirements.txt       # pip fallback
├── simulator.py           # Main simulator script
├── README.md             # Documentation
└── docs/                 # Additional docs
    └── POETRY_GUIDE.md   # This file
```

## 🎯 Use Cases

### Development Testing
```bash
# Single device test
poetry run python simulator.py --device-id dev-test --count 10

# Load testing with multiple devices
for i in {1..5}; do
  poetry run python simulator.py --device-id hive-${i} --interval 2 &
done
```

### CI/CD Integration
```bash
# In CI pipeline
cd firmware
poetry install
poetry run python simulator.py --device-id ci-test --count 5
```

## 🔗 Related Documentation

- **[Backend Poetry Guide](../backend/docs/POETRY_GUIDE.md)** - Complete Poetry tutorial
- **[Telemetry Consumer](../telemetry/docs/POETRY_GUIDE.md)** - MQTT consumer setup
- **[Architecture](../docs/architecture/OVERVIEW.md)** - System overview