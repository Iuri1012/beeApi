# 📡 Telemetry Consumer - Poetry Guide

## 🚀 Quick Start with Poetry

```bash
# Clone and setup
git clone https://github.com/Iuri1012/beeApi.git
cd beeApi/telemetry

# Install with Poetry
poetry install

# Run consumer
poetry shell
python consumer.py
```

## 📦 Dependencies

### Production
- **paho-mqtt 1.6.1** - MQTT client library
- **asyncpg 0.29.0** - Async PostgreSQL driver

### Development  
- **pytest** - Testing framework
- **pytest-asyncio** - Async testing support

## 💻 Development Commands

```bash
# Environment management
poetry install              # Install all dependencies
poetry shell               # Activate virtual environment
poetry env info            # Show environment details

# Running
poetry run python consumer.py           # Run consumer
poetry run python consumer.py --help    # Show help

# Testing (when tests are added)
poetry run pytest          # Run tests
poetry add --group dev coverage  # Add test coverage
poetry run coverage run -m pytest  # Run with coverage

# Dependency management
poetry add paho-mqtt       # Add production dependency
poetry add --group dev black      # Add dev dependency
poetry show                # List all packages
poetry show paho-mqtt      # Show specific package info
poetry update              # Update all dependencies
```

## 🔧 Configuration

### Environment Variables
```bash
# Create .env file
MQTT_BROKER=localhost
MQTT_PORT=1883
DATABASE_URL=postgresql://user:pass@localhost:5433/beeapi_telemetry
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

## 🐳 Docker Integration

### Dockerfile with Poetry
```dockerfile
FROM python:3.9-slim

# Install Poetry
RUN pip install poetry

# Copy Poetry files
COPY pyproject.toml poetry.lock ./

# Configure Poetry (no venv in container)
RUN poetry config virtualenvs.create false

# Install dependencies
RUN poetry install --no-dev

# Copy source
COPY . .

# Run consumer
CMD ["poetry", "run", "python", "consumer.py"]
```

## 🧪 Testing Setup

```bash
# Add testing dependencies
poetry add --group dev pytest-asyncio pytest-mock

# Example test file (tests/test_consumer.py)
poetry run pytest tests/
```

## 🔍 Troubleshooting

### Common Issues

1. **Python version conflict**
   ```bash
   poetry env use python3.9
   poetry install
   ```

2. **Cache issues**
   ```bash
   poetry cache clear pypi --all
   poetry install
   ```

3. **Dependency conflicts**
   ```bash
   poetry update
   poetry lock --no-update
   ```

## 📊 Project Structure

```
telemetry/
├── pyproject.toml          # Poetry configuration
├── poetry.lock            # Lock file
├── requirements.txt       # pip fallback
├── consumer.py            # Main consumer script
├── README.md             # This documentation
└── docs/                 # Additional docs
    └── POETRY_GUIDE.md   # This file
```

## 🔗 Related Documentation

- **[Backend Poetry Guide](../backend/docs/POETRY_GUIDE.md)** - Complete Poetry tutorial
- **[Main Documentation](../docs/README.md)** - Project overview
- **[Architecture](../docs/architecture/OVERVIEW.md)** - System design