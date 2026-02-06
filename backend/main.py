from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import asyncpg
import os

# Import controllers
from controllers import user_controller, bee_controller

# Import Firebase initialization
from config.firebase_config import initialize_firebase, is_firebase_initialized

app = FastAPI(
    title="BeeAPI",
    version="2.0.0",
    description="Multi-user beekeeping management system with Firebase authentication"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database connection pools
pg_pool = None  # PostgreSQL for relational data (apiaries, hives, queens, events)
ts_pool = None  # TimescaleDB for time-series data (telemetry readings)


# Startup/Shutdown events
@app.on_event("startup")
async def startup():
    global pg_pool, ts_pool
    
    # Initialize Firebase
    firebase_app = initialize_firebase()
    if firebase_app:
        print("✓ Firebase initialized successfully")
    else:
        print("⚠ Firebase NOT initialized - check firebase-key.json exists")
        print("  User authentication endpoints will return 503 errors")
    
    # PostgreSQL connection (port 5432) - relational data
    pg_url = os.getenv("POSTGRES_URL", "postgresql://beeapi:beeapi123@localhost:5432/beeapi")
    pg_pool = await asyncpg.create_pool(pg_url, min_size=2, max_size=10)
    print(f"✓ PostgreSQL connection pool created: {pg_url.split('@')[1]}")
    
    # TimescaleDB connection (port 5433) - time-series data
    ts_url = os.getenv("TIMESCALE_URL", "postgresql://beeapi:beeapi123@localhost:5433/beeapi_telemetry")
    ts_pool = await asyncpg.create_pool(ts_url, min_size=2, max_size=10)
    print(f"✓ TimescaleDB connection pool created: {ts_url.split('@')[1]}")
    
    # Set pools in bee_controller only (user_controller uses Firebase/Firestore)
    bee_controller.set_db_pools(pg_pool, ts_pool)
    
    print("✓ Database pools configured in controllers")
    print("")
    print("=== BeeAPI v2.0.0 Started ===")
    print(f"  Firebase: {'Enabled' if is_firebase_initialized() else 'Disabled'}")
    print(f"  PostgreSQL: {pg_url.split('@')[1]}")
    print(f"  TimescaleDB: {ts_url.split('@')[1]}")

@app.on_event("shutdown")
async def shutdown():
    global pg_pool, ts_pool
    if pg_pool:
        await pg_pool.close()
        print("✓ PostgreSQL connection pool closed")
    if ts_pool:
        await ts_pool.close()
        print("✓ TimescaleDB connection pool closed")

# Include routers
app.include_router(user_controller.router)
app.include_router(bee_controller.router)

# API Endpoints
@app.get("/")
async def root():
    return {
        "message": "BeeAPI - Beehive Monitoring System",
        "version": "2.0.0",
        "description": "Multi-user beekeeping management system with apiaries, hives, queens, and event tracking",
        "authentication": "Firebase",
        "firebase_status": "enabled" if is_firebase_initialized() else "disabled"
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "firebase": "connected" if is_firebase_initialized() else "not configured",
        "postgres": "connected" if pg_pool else "disconnected",
        "timescaledb": "connected" if ts_pool else "disconnected"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

