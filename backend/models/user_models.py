"""
User Models

These models are used for user authentication and profile management.
They are designed to be auth-provider agnostic (can work with Firebase, Auth0, custom, etc.)
"""

from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):
    """Model for creating a new user"""
    email: EmailStr
    password: str
    name: str
    phone: Optional[str] = None


class UserLogin(BaseModel):
    """Model for user login"""
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    """Model for updating user profile"""
    name: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None


class UserResponse(BaseModel):
    """Model for user response (excludes sensitive data)"""
    id: str  # Generic id field (could be uid, uuid, etc)
    email: str
    name: str
    phone: Optional[str] = None
    location: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class UserProfile(BaseModel):
    """Model for user profile data"""
    id: str
    email: str
    name: str
    phone: Optional[str] = None
    location: Optional[str] = None
    created_at: str
    updated_at: str


class TokenResponse(BaseModel):
    """Model for authentication token response"""
    access_token: str
    token_type: str = "bearer"
    user_id: str
    email: str
