"""
Authentication Middleware

This module handles token verification and user extraction.
Currently uses Firebase, but can be swapped for any auth provider.
The interface remains the same: extracts user_id from authorization header.
"""

from fastapi import Depends, HTTPException, Header, status
from typing import Optional
import os

# Import Firebase auth (this is the only place outside user_controller that uses Firebase)
try:
    from firebase_admin import auth
    FIREBASE_AVAILABLE = True
except ImportError:
    FIREBASE_AVAILABLE = False


async def get_current_user_id(authorization: Optional[str] = Header(None)) -> str:
    """
    Extract user_id from authorization token.
    
    This middleware is auth-provider agnostic from the caller's perspective.
    It receives a Bearer token and returns a user_id string.
    
    Can be swapped for Auth0, Cognito, custom JWT, etc. by changing
    only this function's implementation.
    
    Args:
        authorization: Bearer token from Authorization header
        
    Returns:
        str: The user's unique identifier
        
    Raises:
        HTTPException: 401 if token is missing or invalid
    """
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authorization header",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    # Extract token from "Bearer <token>" format
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header format. Use: Bearer <token>",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    token = authorization.replace("Bearer ", "")
    
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is empty",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    # Verify token with Firebase
    if not FIREBASE_AVAILABLE:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Authentication service not available"
        )
    
    try:
        # Verify the ID token
        decoded_token = auth.verify_id_token(token)
        user_id = decoded_token['uid']
        return user_id
    except auth.ExpiredIdTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"}
        )
    except auth.RevokedIdTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has been revoked",
            headers={"WWW-Authenticate": "Bearer"}
        )
    except auth.InvalidIdTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"}
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token verification failed: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"}
        )


async def get_optional_user_id(authorization: Optional[str] = Header(None)) -> Optional[str]:
    """
    Optionally extract user_id from authorization token.
    Returns None if no token provided (for public endpoints that
    can optionally be authenticated).
    
    Args:
        authorization: Bearer token from Authorization header (optional)
        
    Returns:
        Optional[str]: The user's unique identifier, or None if not authenticated
    """
    if not authorization:
        return None
    
    try:
        return await get_current_user_id(authorization)
    except HTTPException:
        return None


# Dependency shortcuts for use in route decorators
CurrentUser = Depends(get_current_user_id)
OptionalUser = Depends(get_optional_user_id)
