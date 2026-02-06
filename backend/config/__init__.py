# Config module
from .firebase_config import (
    initialize_firebase,
    get_firestore_client,
    get_auth_client,
    is_firebase_initialized
)

__all__ = [
    "initialize_firebase",
    "get_firestore_client", 
    "get_auth_client",
    "is_firebase_initialized"
]
