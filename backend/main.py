from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import asyncio
import json
from datetime import datetime
import asyncpg
import os

app = FastAPI(title="BeeAPI", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database connection pool
db_pool = None

# WebSocket connections manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, List[WebSocket]] = {}
    
    async def connect(self, websocket: WebSocket, hive_id: str):
        await websocket.accept()
        if hive_id not in self.active_connections:
            self.active_connections[hive_id] = []
        self.active_connections[hive_id].append(websocket)
    
    def disconnect(self, websocket: WebSocket, hive_id: str):
        if hive_id in self.active_connections:
            self.active_connections[hive_id].remove(websocket)
    
    async def broadcast(self, hive_id: str, message: dict):
        if hive_id in self.active_connections:
            for connection in self.active_connections[hive_id]:
                try:
                    await connection.send_json(message)
                except:
                    pass

manager = ConnectionManager()

# Pydantic models
class DeviceRegistration(BaseModel):
    device_id: str
    name: Optional[str] = None
    location: Optional[str] = None

class Hive(BaseModel):
    id: int
    device_id: str
    name: Optional[str]
    location: Optional[str]
    registered_at: datetime

class TelemetryReading(BaseModel):
    time: datetime
    device_id: str
    temperature: Optional[float]
    humidity: Optional[float]
    weight: Optional[float]
    sound_level: Optional[float]

# Startup/Shutdown events
@app.on_event("startup")
async def startup():
    global db_pool
    database_url = os.getenv("DATABASE_URL", "postgresql://beeapi:beeapi123@localhost:5432/beeapi")
    db_pool = await asyncpg.create_pool(database_url, min_size=2, max_size=10)
    print("Database connection pool created")

@app.on_event("shutdown")
async def shutdown():
    global db_pool
    if db_pool:
        await db_pool.close()
        print("Database connection pool closed")

# API Endpoints
@app.get("/")
async def root():
    return {"message": "BeeAPI - Beehive Monitoring System", "version": "1.0.0"}

@app.post("/register-device", response_model=Hive)
async def register_device(device: DeviceRegistration):
    """Register a new beehive device"""
    async with db_pool.acquire() as conn:
        # Check if device already exists
        existing = await conn.fetchrow(
            "SELECT * FROM hives WHERE device_id = $1", device.device_id
        )
        
        if existing:
            raise HTTPException(status_code=400, detail="Device already registered")
        
        # Insert new device
        row = await conn.fetchrow(
            """
            INSERT INTO hives (device_id, name, location)
            VALUES ($1, $2, $3)
            RETURNING id, device_id, name, location, registered_at
            """,
            device.device_id, device.name, device.location
        )
        
        return Hive(**dict(row))

@app.get("/hives", response_model=List[Hive])
async def get_hives():
    """Get all registered hives"""
    async with db_pool.acquire() as conn:
        rows = await conn.fetch("SELECT * FROM hives ORDER BY registered_at DESC")
        return [Hive(**dict(row)) for row in rows]

@app.get("/hives/{device_id}", response_model=Hive)
async def get_hive(device_id: str):
    """Get a specific hive by device_id"""
    async with db_pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT * FROM hives WHERE device_id = $1", device_id
        )
        
        if not row:
            raise HTTPException(status_code=404, detail="Hive not found")
        
        return Hive(**dict(row))

@app.get("/hives/{device_id}/telemetry", response_model=List[TelemetryReading])
async def get_telemetry(device_id: str, limit: int = 100):
    """Get recent telemetry readings for a hive"""
    async with db_pool.acquire() as conn:
        # Verify hive exists
        hive = await conn.fetchrow(
            "SELECT * FROM hives WHERE device_id = $1", device_id
        )
        if not hive:
            raise HTTPException(status_code=404, detail="Hive not found")
        
        # Get telemetry
        rows = await conn.fetch(
            """
            SELECT time, device_id, temperature, humidity, weight, sound_level
            FROM readings
            WHERE device_id = $1
            ORDER BY time DESC
            LIMIT $2
            """,
            device_id, limit
        )
        
        return [TelemetryReading(**dict(row)) for row in rows]

@app.websocket("/ws/hive/{device_id}/telemetry")
async def websocket_telemetry(websocket: WebSocket, device_id: str):
    """WebSocket endpoint for real-time telemetry"""
    await manager.connect(websocket, device_id)
    
    try:
        # Send recent readings on connect
        async with db_pool.acquire() as conn:
            rows = await conn.fetch(
                """
                SELECT time, device_id, temperature, humidity, weight, sound_level
                FROM readings
                WHERE device_id = $1
                ORDER BY time DESC
                LIMIT 10
                """,
                device_id
            )
            
            for row in reversed(rows):
                reading = TelemetryReading(**dict(row))
                await websocket.send_json(reading.dict(default=str))
        
        # Keep connection alive and wait for messages
        while True:
            # Just receive and ignore client messages (ping/pong)
            try:
                data = await asyncio.wait_for(websocket.receive_text(), timeout=30.0)
            except asyncio.TimeoutError:
                # Send ping to keep connection alive
                await websocket.send_json({"type": "ping"})
                
    except WebSocketDisconnect:
        manager.disconnect(websocket, device_id)
        print(f"WebSocket disconnected for device {device_id}")
    except Exception as e:
        print(f"WebSocket error: {e}")
        manager.disconnect(websocket, device_id)

# Function to broadcast telemetry (called by telemetry consumer)
async def broadcast_telemetry(device_id: str, telemetry: dict):
    """Broadcast telemetry to connected WebSocket clients"""
    await manager.broadcast(device_id, telemetry)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
