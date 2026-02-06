"""
Bee Controller

This controller handles all bee management operations:
- Apiaries (create, read, update, delete)
- Hives (create, read, update, delete)
- Queen Bees (create, read, update, delete)
- Events (create, read, delete)
- Telemetry (read, WebSocket)

IMPORTANT: This controller is database-agnostic regarding authentication.
It receives user_id as a string from the auth middleware and does NOT import Firebase.
"""

from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect, Depends, Query
from typing import List, Optional
import asyncpg
import asyncio
from models import (
    Apiary, ApiaryCreate, ApiaryUpdate,
    Hive, HiveCreate, HiveUpdate,
    QueenBee, QueenBeeCreate, QueenBeeUpdate,
    Event, EventCreate,
    TelemetryReading
)
from middleware.auth import get_current_user_id, get_optional_user_id

router = APIRouter(tags=["bee management"])

# Database pools
pg_pool = None  # PostgreSQL for relational data (apiaries, hives, queens, events)
ts_pool = None  # TimescaleDB for time-series data (telemetry readings)

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


def set_db_pools(postgres_pool, timescale_pool):
    """Set both database pools - PostgreSQL and TimescaleDB"""
    global pg_pool, ts_pool
    pg_pool = postgres_pool
    ts_pool = timescale_pool


# ==================== APIARY ENDPOINTS ====================

@router.post("/apiaries", response_model=Apiary)
async def create_apiary(
    apiary: ApiaryCreate,
    user_id: str = Depends(get_current_user_id)
):
    """Create a new apiary for the authenticated user"""
    async with pg_pool.acquire() as conn:
        row = await conn.fetchrow(
            """
            INSERT INTO apiaries (name, location, user_id)
            VALUES ($1, $2, $3)
            RETURNING id, name, location, user_id, created_at, updated_at
            """,
            apiary.name, apiary.location, user_id
        )
        
        return Apiary(**dict(row))


@router.get("/apiaries", response_model=List[Apiary])
async def get_apiaries(user_id: str = Depends(get_current_user_id)):
    """Get all apiaries for the authenticated user"""
    async with pg_pool.acquire() as conn:
        rows = await conn.fetch(
            "SELECT * FROM apiaries WHERE user_id = $1 ORDER BY created_at DESC",
            user_id
        )
        
        return [Apiary(**dict(row)) for row in rows]


@router.get("/apiaries/{apiary_id}", response_model=Apiary)
async def get_apiary(
    apiary_id: int,
    user_id: str = Depends(get_current_user_id)
):
    """Get a specific apiary (must belong to authenticated user)"""
    async with pg_pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT * FROM apiaries WHERE id = $1 AND user_id = $2",
            apiary_id, user_id
        )
        
        if not row:
            raise HTTPException(status_code=404, detail="Apiary not found")
        
        return Apiary(**dict(row))


@router.put("/apiaries/{apiary_id}", response_model=Apiary)
async def update_apiary(
    apiary_id: int,
    apiary_update: ApiaryUpdate,
    user_id: str = Depends(get_current_user_id)
):
    """Update an apiary (must belong to authenticated user)"""
    async with pg_pool.acquire() as conn:
        existing = await conn.fetchrow(
            "SELECT * FROM apiaries WHERE id = $1 AND user_id = $2",
            apiary_id, user_id
        )
        if not existing:
            raise HTTPException(status_code=404, detail="Apiary not found")
        
        update_fields = []
        params = []
        param_count = 1
        
        if apiary_update.name is not None:
            update_fields.append(f"name = ${param_count}")
            params.append(apiary_update.name)
            param_count += 1
        
        if apiary_update.location is not None:
            update_fields.append(f"location = ${param_count}")
            params.append(apiary_update.location)
            param_count += 1
        
        if not update_fields:
            raise HTTPException(status_code=400, detail="No fields to update")
        
        update_fields.append("updated_at = CURRENT_TIMESTAMP")
        params.append(apiary_id)
        
        query = f"""
            UPDATE apiaries
            SET {', '.join(update_fields)}
            WHERE id = ${param_count}
            RETURNING id, name, location, user_id, created_at, updated_at
        """
        
        row = await conn.fetchrow(query, *params)
        return Apiary(**dict(row))


@router.delete("/apiaries/{apiary_id}")
async def delete_apiary(
    apiary_id: int,
    user_id: str = Depends(get_current_user_id)
):
    """Delete an apiary (must belong to authenticated user)"""
    async with pg_pool.acquire() as conn:
        existing = await conn.fetchrow(
            "SELECT * FROM apiaries WHERE id = $1 AND user_id = $2",
            apiary_id, user_id
        )
        if not existing:
            raise HTTPException(status_code=404, detail="Apiary not found")
        
        await conn.execute("DELETE FROM apiaries WHERE id = $1", apiary_id)
        return {"message": "Apiary deleted successfully"}


# ==================== HIVE ENDPOINTS ====================

async def _verify_apiary_ownership(conn, apiary_id: int, user_id: str):
    """Helper to verify apiary belongs to user"""
    apiary = await conn.fetchrow(
        "SELECT * FROM apiaries WHERE id = $1 AND user_id = $2",
        apiary_id, user_id
    )
    if not apiary:
        raise HTTPException(status_code=404, detail="Apiary not found")
    return apiary


async def _verify_hive_ownership(conn, hive_id: int, user_id: str):
    """Helper to verify hive belongs to user (through apiary)"""
    hive = await conn.fetchrow(
        """
        SELECT h.* FROM hives h
        JOIN apiaries a ON h.apiary_id = a.id
        WHERE h.id = $1 AND a.user_id = $2
        """,
        hive_id, user_id
    )
    if not hive:
        raise HTTPException(status_code=404, detail="Hive not found")
    return hive


@router.post("/apiaries/{apiary_id}/hives", response_model=Hive)
async def create_hive(
    apiary_id: int,
    hive: HiveCreate,
    user_id: str = Depends(get_current_user_id)
):
    """Create a new hive in an apiary (apiary must belong to authenticated user)"""
    async with pg_pool.acquire() as conn:
        # Verify apiary ownership
        await _verify_apiary_ownership(conn, apiary_id, user_id)
        
        # Check if device_id already exists
        existing = await conn.fetchrow("SELECT * FROM hives WHERE device_id = $1", hive.device_id)
        if existing:
            raise HTTPException(status_code=400, detail="Device ID already registered")
        
        row = await conn.fetchrow(
            """
            INSERT INTO hives (device_id, name, apiary_id)
            VALUES ($1, $2, $3)
            RETURNING id, device_id, name, apiary_id, current_queen_id, created_at, updated_at
            """,
            hive.device_id, hive.name, apiary_id
        )
        
        return Hive(**dict(row))


@router.get("/apiaries/{apiary_id}/hives", response_model=List[Hive])
async def get_hives_by_apiary(
    apiary_id: int,
    user_id: str = Depends(get_current_user_id)
):
    """Get all hives for an apiary (apiary must belong to authenticated user)"""
    async with pg_pool.acquire() as conn:
        # Verify apiary ownership
        await _verify_apiary_ownership(conn, apiary_id, user_id)
        
        rows = await conn.fetch(
            "SELECT * FROM hives WHERE apiary_id = $1 ORDER BY created_at DESC",
            apiary_id
        )
        
        return [Hive(**dict(row)) for row in rows]


@router.get("/hives", response_model=List[Hive])
async def get_all_hives(user_id: str = Depends(get_current_user_id)):
    """Get all hives for the authenticated user (across all apiaries)"""
    async with pg_pool.acquire() as conn:
        rows = await conn.fetch(
            """
            SELECT h.* FROM hives h
            JOIN apiaries a ON h.apiary_id = a.id
            WHERE a.user_id = $1
            ORDER BY h.created_at DESC
            """,
            user_id
        )
        
        return [Hive(**dict(row)) for row in rows]


@router.get("/hives/{hive_id}", response_model=Hive)
async def get_hive(
    hive_id: int,
    user_id: str = Depends(get_current_user_id)
):
    """Get a specific hive (must belong to authenticated user)"""
    async with pg_pool.acquire() as conn:
        row = await _verify_hive_ownership(conn, hive_id, user_id)
        return Hive(**dict(row))


@router.put("/hives/{hive_id}", response_model=Hive)
async def update_hive(
    hive_id: int,
    hive_update: HiveUpdate,
    user_id: str = Depends(get_current_user_id)
):
    """Update a hive (must belong to authenticated user)"""
    async with pg_pool.acquire() as conn:
        existing = await _verify_hive_ownership(conn, hive_id, user_id)
        
        update_fields = []
        params = []
        param_count = 1
        
        if hive_update.device_id is not None:
            update_fields.append(f"device_id = ${param_count}")
            params.append(hive_update.device_id)
            param_count += 1
        
        if hive_update.name is not None:
            update_fields.append(f"name = ${param_count}")
            params.append(hive_update.name)
            param_count += 1
        
        if hive_update.apiary_id is not None:
            # Verify new apiary belongs to user
            await _verify_apiary_ownership(conn, hive_update.apiary_id, user_id)
            
            update_fields.append(f"apiary_id = ${param_count}")
            params.append(hive_update.apiary_id)
            param_count += 1
        
        if not update_fields:
            raise HTTPException(status_code=400, detail="No fields to update")
        
        update_fields.append("updated_at = CURRENT_TIMESTAMP")
        params.append(hive_id)
        
        query = f"""
            UPDATE hives
            SET {', '.join(update_fields)}
            WHERE id = ${param_count}
            RETURNING id, device_id, name, apiary_id, current_queen_id, created_at, updated_at
        """
        
        row = await conn.fetchrow(query, *params)
        return Hive(**dict(row))


@router.delete("/hives/{hive_id}")
async def delete_hive(
    hive_id: int,
    user_id: str = Depends(get_current_user_id)
):
    """Delete a hive (must belong to authenticated user)"""
    async with pg_pool.acquire() as conn:
        await _verify_hive_ownership(conn, hive_id, user_id)
        
        await conn.execute("DELETE FROM hives WHERE id = $1", hive_id)
        return {"message": "Hive deleted successfully"}


# ==================== QUEEN BEE ENDPOINTS ====================

@router.post("/hives/{hive_id}/queens", response_model=QueenBee)
async def create_queen_bee(
    hive_id: int,
    queen: QueenBeeCreate,
    user_id: str = Depends(get_current_user_id)
):
    """Introduce a new queen bee to a hive (hive must belong to authenticated user)"""
    async with pg_pool.acquire() as conn:
        # Verify hive ownership
        hive = await _verify_hive_ownership(conn, hive_id, user_id)
        
        # Retire current queen if exists
        if hive['current_queen_id']:
            await conn.execute(
                "UPDATE queen_bees SET retired_date = CURRENT_TIMESTAMP WHERE id = $1",
                hive['current_queen_id']
            )
        
        # Insert new queen
        row = await conn.fetchrow(
            """
            INSERT INTO queen_bees (name, breed, birth_date, hive_id)
            VALUES ($1, $2, $3, $4)
            RETURNING id, name, breed, birth_date, introduced_date, retired_date, hive_id
            """,
            queen.name, queen.breed, queen.birth_date, hive_id
        )
        
        # Update hive's current_queen_id
        await conn.execute(
            "UPDATE hives SET current_queen_id = $1, updated_at = CURRENT_TIMESTAMP WHERE id = $2",
            row['id'], hive_id
        )
        
        return QueenBee(**dict(row))


@router.get("/hives/{hive_id}/queens", response_model=List[QueenBee])
async def get_hive_queens(
    hive_id: int,
    user_id: str = Depends(get_current_user_id)
):
    """Get all queens for a hive (current and historical)"""
    async with pg_pool.acquire() as conn:
        # Verify hive ownership
        await _verify_hive_ownership(conn, hive_id, user_id)
        
        rows = await conn.fetch(
            "SELECT * FROM queen_bees WHERE hive_id = $1 ORDER BY introduced_date DESC",
            hive_id
        )
        return [QueenBee(**dict(row)) for row in rows]


@router.get("/queens/{queen_id}", response_model=QueenBee)
async def get_queen_bee(
    queen_id: int,
    user_id: str = Depends(get_current_user_id)
):
    """Get a specific queen bee (must belong to authenticated user's hive)"""
    async with pg_pool.acquire() as conn:
        row = await conn.fetchrow(
            """
            SELECT q.* FROM queen_bees q
            JOIN hives h ON q.hive_id = h.id
            JOIN apiaries a ON h.apiary_id = a.id
            WHERE q.id = $1 AND a.user_id = $2
            """,
            queen_id, user_id
        )
        
        if not row:
            raise HTTPException(status_code=404, detail="Queen bee not found")
        
        return QueenBee(**dict(row))


@router.put("/queens/{queen_id}", response_model=QueenBee)
async def update_queen_bee(
    queen_id: int,
    queen_update: QueenBeeUpdate,
    user_id: str = Depends(get_current_user_id)
):
    """Update a queen bee (must belong to authenticated user's hive)"""
    async with pg_pool.acquire() as conn:
        existing = await conn.fetchrow(
            """
            SELECT q.* FROM queen_bees q
            JOIN hives h ON q.hive_id = h.id
            JOIN apiaries a ON h.apiary_id = a.id
            WHERE q.id = $1 AND a.user_id = $2
            """,
            queen_id, user_id
        )
        if not existing:
            raise HTTPException(status_code=404, detail="Queen bee not found")
        
        update_fields = []
        params = []
        param_count = 1
        
        if queen_update.name is not None:
            update_fields.append(f"name = ${param_count}")
            params.append(queen_update.name)
            param_count += 1
        
        if queen_update.breed is not None:
            update_fields.append(f"breed = ${param_count}")
            params.append(queen_update.breed)
            param_count += 1
        
        if queen_update.birth_date is not None:
            update_fields.append(f"birth_date = ${param_count}")
            params.append(queen_update.birth_date)
            param_count += 1
        
        if queen_update.retired_date is not None:
            update_fields.append(f"retired_date = ${param_count}")
            params.append(queen_update.retired_date)
            param_count += 1
        
        if not update_fields:
            raise HTTPException(status_code=400, detail="No fields to update")
        
        params.append(queen_id)
        
        query = f"""
            UPDATE queen_bees
            SET {', '.join(update_fields)}
            WHERE id = ${param_count}
            RETURNING id, name, breed, birth_date, introduced_date, retired_date, hive_id
        """
        
        row = await conn.fetchrow(query, *params)
        return QueenBee(**dict(row))


@router.delete("/queens/{queen_id}")
async def delete_queen_bee(
    queen_id: int,
    user_id: str = Depends(get_current_user_id)
):
    """Delete a queen bee record (must belong to authenticated user's hive)"""
    async with pg_pool.acquire() as conn:
        existing = await conn.fetchrow(
            """
            SELECT q.* FROM queen_bees q
            JOIN hives h ON q.hive_id = h.id
            JOIN apiaries a ON h.apiary_id = a.id
            WHERE q.id = $1 AND a.user_id = $2
            """,
            queen_id, user_id
        )
        if not existing:
            raise HTTPException(status_code=404, detail="Queen bee not found")
        
        # Check if this is the current queen of a hive
        hive = await conn.fetchrow("SELECT * FROM hives WHERE current_queen_id = $1", queen_id)
        if hive:
            await conn.execute(
                "UPDATE hives SET current_queen_id = NULL WHERE id = $1",
                hive['id']
            )
        
        await conn.execute("DELETE FROM queen_bees WHERE id = $1", queen_id)
        return {"message": "Queen bee deleted successfully"}


# ==================== EVENT ENDPOINTS ====================

@router.post("/hives/{hive_id}/events", response_model=Event)
async def create_hive_event(
    hive_id: int,
    event: EventCreate,
    user_id: str = Depends(get_current_user_id)
):
    """Create a new event for a hive (hive must belong to authenticated user)"""
    async with pg_pool.acquire() as conn:
        # Verify hive ownership
        await _verify_hive_ownership(conn, hive_id, user_id)
        
        row = await conn.fetchrow(
            """
            INSERT INTO events (description, hive_id)
            VALUES ($1, $2)
            RETURNING id, date, description, hive_id, apiary_id
            """,
            event.description, hive_id
        )
        
        return Event(**dict(row))


@router.get("/hives/{hive_id}/events", response_model=List[Event])
async def get_hive_events(
    hive_id: int,
    user_id: str = Depends(get_current_user_id)
):
    """Get all events for a hive (hive must belong to authenticated user)"""
    async with pg_pool.acquire() as conn:
        # Verify hive ownership
        await _verify_hive_ownership(conn, hive_id, user_id)
        
        rows = await conn.fetch(
            "SELECT * FROM events WHERE hive_id = $1 ORDER BY date DESC",
            hive_id
        )
        return [Event(**dict(row)) for row in rows]


@router.post("/apiaries/{apiary_id}/events", response_model=Event)
async def create_apiary_event(
    apiary_id: int,
    event: EventCreate,
    user_id: str = Depends(get_current_user_id)
):
    """Create a new event for an apiary (apiary must belong to authenticated user)"""
    async with pg_pool.acquire() as conn:
        # Verify apiary ownership
        await _verify_apiary_ownership(conn, apiary_id, user_id)
        
        row = await conn.fetchrow(
            """
            INSERT INTO events (description, apiary_id)
            VALUES ($1, $2)
            RETURNING id, date, description, hive_id, apiary_id
            """,
            event.description, apiary_id
        )
        
        return Event(**dict(row))


@router.get("/apiaries/{apiary_id}/events", response_model=List[Event])
async def get_apiary_events(
    apiary_id: int,
    user_id: str = Depends(get_current_user_id)
):
    """Get all events for an apiary (apiary must belong to authenticated user)"""
    async with pg_pool.acquire() as conn:
        # Verify apiary ownership
        await _verify_apiary_ownership(conn, apiary_id, user_id)
        
        rows = await conn.fetch(
            "SELECT * FROM events WHERE apiary_id = $1 ORDER BY date DESC",
            apiary_id
        )
        return [Event(**dict(row)) for row in rows]


@router.delete("/events/{event_id}")
async def delete_event(
    event_id: int,
    user_id: str = Depends(get_current_user_id)
):
    """Delete an event (must belong to authenticated user's apiary/hive)"""
    async with pg_pool.acquire() as conn:
        # Check if event exists and belongs to user
        existing = await conn.fetchrow(
            """
            SELECT e.* FROM events e
            LEFT JOIN hives h ON e.hive_id = h.id
            LEFT JOIN apiaries a_hive ON h.apiary_id = a_hive.id
            LEFT JOIN apiaries a_direct ON e.apiary_id = a_direct.id
            WHERE e.id = $1 AND (a_hive.user_id = $2 OR a_direct.user_id = $2)
            """,
            event_id, user_id
        )
        if not existing:
            raise HTTPException(status_code=404, detail="Event not found")
        
        await conn.execute("DELETE FROM events WHERE id = $1", event_id)
        return {"message": "Event deleted successfully"}


@router.put("/events/{event_id}", response_model=Event)
async def update_event(
    event_id: int,
    event: EventCreate,
    user_id: str = Depends(get_current_user_id)
):
    """Update an event (must belong to authenticated user's apiary/hive)"""
    async with pg_pool.acquire() as conn:
        # Check if event exists and belongs to user
        existing = await conn.fetchrow(
            """
            SELECT e.* FROM events e
            LEFT JOIN hives h ON e.hive_id = h.id
            LEFT JOIN apiaries a_hive ON h.apiary_id = a_hive.id
            LEFT JOIN apiaries a_direct ON e.apiary_id = a_direct.id
            WHERE e.id = $1 AND (a_hive.user_id = $2 OR a_direct.user_id = $2)
            """,
            event_id, user_id
        )
        if not existing:
            raise HTTPException(status_code=404, detail="Event not found")
        
        # Update the event
        row = await conn.fetchrow(
            """
            UPDATE events 
            SET description = $2
            WHERE id = $1
            RETURNING id, date, description, hive_id, apiary_id
            """,
            event_id, event.description
        )
        
        return Event(**dict(row))


# ==================== TELEMETRY ENDPOINTS ====================

@router.get("/hives/{hive_id}/telemetry", response_model=List[TelemetryReading])
async def get_hive_telemetry(
    hive_id: int,
    limit: int = 100,
    user_id: str = Depends(get_current_user_id)
):
    """Get recent telemetry readings for a hive (hive must belong to authenticated user)"""
    # Get hive info from PostgreSQL and verify ownership
    async with pg_pool.acquire() as conn:
        hive = await _verify_hive_ownership(conn, hive_id, user_id)
        device_id = hive['device_id']
    
    # Get telemetry from TimescaleDB
    async with ts_pool.acquire() as conn:
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


@router.websocket("/ws/hive/{hive_id}/telemetry")
async def websocket_telemetry(websocket: WebSocket, hive_id: int):
    """WebSocket endpoint for real-time telemetry"""
    # Get hive info from PostgreSQL
    async with pg_pool.acquire() as conn:
        hive = await conn.fetchrow("SELECT * FROM hives WHERE id = $1", hive_id)
        if not hive:
            await websocket.close(code=1008, reason="Hive not found")
            return
        
        device_id = hive['device_id']
    
    await manager.connect(websocket, device_id)
    
    try:
        # Send recent readings on connect from TimescaleDB
        async with ts_pool.acquire() as conn:
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
            try:
                data = await asyncio.wait_for(websocket.receive_text(), timeout=30.0)
            except asyncio.TimeoutError:
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
