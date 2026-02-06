"""
User Controller

This controller handles user authentication and profile management.
It uses Firebase Authentication and Firestore for user data.

IMPORTANT: This is the ONLY controller that references Firebase directly.
All other controllers use generic user_id from the auth middleware.
"""

from fastapi import APIRouter, HTTPException, Depends, status
from typing import List, Optional
from datetime import datetime
import os

# Firebase imports (isolated to this controller)
try:
    from firebase_admin import auth, firestore
    from config.firebase_config import get_firestore_client, get_auth_client, is_firebase_initialized
    FIREBASE_AVAILABLE = True
except ImportError:
    FIREBASE_AVAILABLE = False

from models import UserCreate, UserLogin, UserUpdate, UserResponse, UserProfile, TokenResponse
from middleware.auth import get_current_user_id

router = APIRouter(prefix="/users", tags=["users"])


def _get_db():
    """Get Firestore client"""
    if not FIREBASE_AVAILABLE or not is_firebase_initialized():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Firebase service not available"
        )
    return get_firestore_client()


def _get_auth():
    """Get Firebase Auth client"""
    if not FIREBASE_AVAILABLE or not is_firebase_initialized():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Firebase service not available"
        )
    return get_auth_client()


@router.post("/register", response_model=TokenResponse)
async def register_user(user: UserCreate):
    """
    Register a new user.
    
    Creates a Firebase Authentication user and a Firestore profile document.
    
    Args:
        user: User registration data (email, password, name, optional phone)
        
    Returns:
        TokenResponse with access_token, user_id, and email
    """
    auth_client = _get_auth()
    db = _get_db()
    
    try:
        # Create Firebase Authentication user
        firebase_user = auth_client.create_user(
            email=user.email,
            password=user.password,
            display_name=user.name
        )
        
        # Create Firestore user profile document
        user_doc = {
            "email": user.email,
            "name": user.name,
            "phone": user.phone or "",
            "location": "",
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat()
        }
        
        db.collection("users").document(firebase_user.uid).set(user_doc)
        
        # Generate custom token for the user
        custom_token = auth_client.create_custom_token(firebase_user.uid)
        
        return TokenResponse(
            access_token=custom_token.decode() if isinstance(custom_token, bytes) else custom_token,
            token_type="bearer",
            user_id=firebase_user.uid,
            email=user.email
        )
        
    except auth.EmailAlreadyExistsError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create user: {str(e)}"
        )


@router.post("/login")
async def login_user(user: UserLogin):
    """
    Login a user.
    
    Note: Firebase Admin SDK cannot verify passwords directly.
    This endpoint returns user info if the email exists.
    For full login flow, use Firebase Client SDK on the frontend.
    
    Args:
        user: Login credentials (email, password)
        
    Returns:
        User info and instructions for client-side authentication
    """
    auth_client = _get_auth()
    
    try:
        # Get user by email to verify they exist
        firebase_user = auth_client.get_user_by_email(user.email)
        
        # Note: Firebase Admin SDK cannot verify passwords
        # The frontend should use Firebase Client SDK for actual login
        return {
            "message": "User exists. Use Firebase Client SDK for authentication.",
            "user_id": firebase_user.uid,
            "email": firebase_user.email,
            "hint": "Call Firebase signInWithEmailAndPassword() from your client app"
        }
        
    except auth.UserNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Login failed: {str(e)}"
        )


@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(user_id: str = Depends(get_current_user_id)):
    """
    Get the current authenticated user's profile.
    
    Requires valid Bearer token in Authorization header.
    
    Returns:
        UserResponse with user profile data
    """
    db = _get_db()
    
    doc = db.collection("users").document(user_id).get()
    
    if not doc.exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User profile not found"
        )
    
    user_data = doc.to_dict()
    
    # Parse dates
    created_at = datetime.fromisoformat(user_data.get("created_at", datetime.utcnow().isoformat()))
    updated_at_str = user_data.get("updated_at")
    updated_at = datetime.fromisoformat(updated_at_str) if updated_at_str else None
    
    return UserResponse(
        id=user_id,
        email=user_data.get("email", ""),
        name=user_data.get("name", ""),
        phone=user_data.get("phone"),
        location=user_data.get("location"),
        created_at=created_at,
        updated_at=updated_at
    )


@router.put("/me", response_model=UserResponse)
async def update_current_user_profile(
    user_update: UserUpdate,
    user_id: str = Depends(get_current_user_id)
):
    """
    Update the current authenticated user's profile.
    
    Requires valid Bearer token in Authorization header.
    
    Args:
        user_update: Fields to update (name, phone, location)
        
    Returns:
        Updated UserResponse
    """
    db = _get_db()
    auth_client = _get_auth()
    
    # Check if user exists
    doc_ref = db.collection("users").document(user_id)
    doc = doc_ref.get()
    
    if not doc.exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User profile not found"
        )
    
    # Build update data (only include non-None fields)
    update_data = user_update.dict(exclude_unset=True)
    update_data["updated_at"] = datetime.utcnow().isoformat()
    
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields to update"
        )
    
    # Update Firestore document
    doc_ref.update(update_data)
    
    # If name was updated, also update Firebase Auth display name
    if user_update.name:
        try:
            auth_client.update_user(user_id, display_name=user_update.name)
        except Exception:
            pass  # Non-critical, Firestore is source of truth
    
    # Return updated profile
    return await get_current_user_profile(user_id)


@router.delete("/me")
async def delete_current_user(user_id: str = Depends(get_current_user_id)):
    """
    Delete the current authenticated user's account.
    
    This will:
    1. Delete the Firebase Authentication user
    2. Delete the Firestore user profile document
    
    Note: Associated apiaries, hives, etc. in PostgreSQL are NOT automatically deleted.
    You may want to clean those up separately or handle via API.
    
    Requires valid Bearer token in Authorization header.
    
    Returns:
        Success message
    """
    db = _get_db()
    auth_client = _get_auth()
    
    try:
        # Delete Firestore profile
        db.collection("users").document(user_id).delete()
        
        # Delete Firebase Authentication user
        auth_client.delete_user(user_id)
        
        return {"message": "User account deleted successfully"}
        
    except auth.UserNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete user: {str(e)}"
        )


@router.get("/{user_id}", response_model=UserResponse)
async def get_user_by_id(
    user_id: str,
    current_user_id: str = Depends(get_current_user_id)
):
    """
    Get a user's public profile by ID.
    
    Requires authentication.
    
    Args:
        user_id: The user ID to look up
        
    Returns:
        UserResponse with user profile data
    """
    db = _get_db()
    
    doc = db.collection("users").document(user_id).get()
    
    if not doc.exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    user_data = doc.to_dict()
    
    # Parse dates
    created_at = datetime.fromisoformat(user_data.get("created_at", datetime.utcnow().isoformat()))
    updated_at_str = user_data.get("updated_at")
    updated_at = datetime.fromisoformat(updated_at_str) if updated_at_str else None
    
    return UserResponse(
        id=user_id,
        email=user_data.get("email", ""),
        name=user_data.get("name", ""),
        phone=user_data.get("phone"),
        location=user_data.get("location"),
        created_at=created_at,
        updated_at=updated_at
    )
