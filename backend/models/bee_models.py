"""
Bee Management Models

These models are DATABASE-AGNOSTIC and AUTH-PROVIDER AGNOSTIC.
They use generic field names (user_id) that work with any
authentication system (Firebase, Auth0, custom, etc.) and any database.

NO Firebase-specific imports or references should be in this file.
"""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# ==================== EVENT MODELS ====================

class EventCreate(BaseModel):
    """Model for creating a new event"""
    description: str


class Event(BaseModel):
    """
    Event model - can be attached to either a hive or apiary.
    Only one of hive_id or apiary_id will be set.
    """
    id: int
    date: datetime
    description: str
    hive_id: Optional[int] = None
    apiary_id: Optional[int] = None

    class Config:
        from_attributes = True


# ==================== QUEEN BEE MODELS ====================

class QueenBeeCreate(BaseModel):
    """Model for introducing a new queen bee"""
    name: Optional[str] = None
    breed: Optional[str] = None
    birth_date: Optional[datetime] = None


class QueenBeeUpdate(BaseModel):
    """Model for updating queen bee information"""
    name: Optional[str] = None
    breed: Optional[str] = None
    birth_date: Optional[datetime] = None
    retired_date: Optional[datetime] = None


class QueenBee(BaseModel):
    """Queen bee model with full details"""
    id: int
    name: Optional[str] = None
    breed: Optional[str] = None
    birth_date: Optional[datetime] = None
    introduced_date: datetime
    retired_date: Optional[datetime] = None
    hive_id: int

    class Config:
        from_attributes = True


# ==================== HIVE MODELS ====================

class HiveCreate(BaseModel):
    """Model for creating a new hive"""
    device_id: str
    name: Optional[str] = None


class HiveUpdate(BaseModel):
    """Model for updating hive information"""
    device_id: Optional[str] = None
    name: Optional[str] = None
    apiary_id: Optional[int] = None


class Hive(BaseModel):
    """Hive model with full details"""
    id: int
    device_id: str
    name: Optional[str] = None
    apiary_id: int
    current_queen_id: Optional[int] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ==================== APIARY MODELS ====================

class ApiaryCreate(BaseModel):
    """
    Model for creating a new apiary.
    Note: user_id is NOT included here - it's extracted from auth middleware.
    """
    name: str
    location: Optional[str] = None


class ApiaryUpdate(BaseModel):
    """Model for updating apiary information"""
    name: Optional[str] = None
    location: Optional[str] = None


class Apiary(BaseModel):
    """
    Apiary model with full details.
    user_id is a generic string - works with any auth system.
    """
    id: int
    user_id: str  # Generic user_id (could be Firebase uid, Auth0 id, UUID, etc.)
    name: str
    location: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ==================== TELEMETRY MODELS ====================

class TelemetryReading(BaseModel):
    """Model for sensor telemetry data"""
    time: datetime
    device_id: str
    temperature: Optional[float] = None
    humidity: Optional[float] = None
    weight: Optional[float] = None
    sound_level: Optional[float] = None

    class Config:
        from_attributes = True
