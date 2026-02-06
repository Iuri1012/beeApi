FROM python:3.11-slim

WORKDIR /app

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

# Since we disabled virtualenvs, we can run python directly
CMD ["python", "consumer.py"]
