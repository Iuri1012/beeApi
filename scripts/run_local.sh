#!/bin/bash

set -e

echo "🐝 Starting BeeAPI Local Environment..."

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Checking prerequisites...${NC}"

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker and try again."
    exit 1
fi

echo -e "${GREEN}✓ Docker is running${NC}"

# Check if docker compose exists
if ! docker compose version &> /dev/null; then
    echo "❌ docker compose not found. Please install docker compose."
    exit 1
fi

echo -e "${GREEN}✓ docker compose found${NC}"

# Stop any existing containers
echo -e "${YELLOW}Stopping any existing containers...${NC}"
docker compose down 2>/dev/null || true

# Start services
echo -e "${YELLOW}Starting services with docker compose...${NC}"
docker compose up -d

# Wait for services to be ready
echo -e "${YELLOW}Waiting for services to be ready...${NC}"

# Wait for PostgreSQL
echo "Waiting for PostgreSQL..."
for i in {1..30}; do
    if docker compose exec -T postgres pg_isready -U beeapi > /dev/null 2>&1; then
        echo -e "${GREEN}✓ PostgreSQL is ready${NC}"
        break
    fi
    if [ $i -eq 30 ]; then
        echo "❌ PostgreSQL failed to start in time"
        docker compose logs postgres
        exit 1
    fi
    sleep 1
done

# Wait for backend
echo "Waiting for backend..."
for i in {1..60}; do
    if curl -s http://localhost:8000/ > /dev/null 2>&1; then
        echo -e "${GREEN}✓ Backend is ready${NC}"
        break
    fi
    if [ $i -eq 60 ]; then
        echo "❌ Backend failed to start in time"
        docker compose logs backend
        exit 1
    fi
    sleep 1
done

# Wait for web
echo "Waiting for web dashboard..."
for i in {1..90}; do
    if curl -s http://localhost:3000/ > /dev/null 2>&1; then
        echo -e "${GREEN}✓ Web dashboard is ready${NC}"
        break
    fi
    if [ $i -eq 90 ]; then
        echo "⚠️  Web dashboard may still be starting (this is normal on first run)"
        break
    fi
    sleep 1
done

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}🎉 BeeAPI is running!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "📊 Web Dashboard: http://localhost:3000"
echo "🔌 API Server:    http://localhost:8000"
echo "📖 API Docs:      http://localhost:8000/docs"
echo "🦟 MQTT Broker:   localhost:1883"
echo ""
echo -e "${YELLOW}Starting firmware simulator...${NC}"
echo ""

# Check if Python is available
if command -v python3 &> /dev/null; then
    # Install dependencies if needed
    if [ ! -d "firmware/venv" ]; then
        echo "Creating Python virtual environment..."
        cd firmware
        python3 -m venv venv
        source venv/bin/activate
        pip install -r requirements.txt > /dev/null 2>&1
        cd ..
    fi
    
    # Run simulator
    echo -e "${GREEN}Running simulator for device hive-001...${NC}"
    echo "Press Ctrl+C to stop the simulator and view logs"
    echo ""
    
    cd firmware
    source venv/bin/activate
    python simulator.py --device-id hive-001 --broker localhost --interval 5
else
    echo "⚠️  Python3 not found. Please install Python to run the simulator."
    echo ""
    echo "To run simulator manually:"
    echo "  cd firmware"
    echo "  pip install -r requirements.txt"
    echo "  python simulator.py --device-id hive-001 --broker localhost"
fi

echo ""
echo -e "${YELLOW}To stop all services:${NC}"
echo "  docker compose down"
echo ""
echo -e "${YELLOW}To view logs:${NC}"
echo "  docker compose logs -f [service-name]"
echo ""
