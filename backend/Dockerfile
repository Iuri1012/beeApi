FROM python:3.11-slim

WORKDIR /app

# Install system dependencies including curl for health checks
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install poetry

# Copy Poetry configuration
COPY pyproject.toml poetry.lock* ./

# Configure Poetry: Don't create a virtual environment (we're in a container)
RUN poetry config virtualenvs.create false

# Install dependencies (production only)
RUN poetry install --without dev --no-interaction --no-ansi

# Copy application code
COPY . .

# Since we disabled virtualenvs, we can run uvicorn directly
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
