"""
Firebase Configuration Module

This module initializes Firebase Admin SDK for authentication and Firestore.
Only this module and user_controller.py reference Firebase directly.
All other modules remain database-agnostic.
"""

import firebase_admin
from firebase_admin import credentials, auth, firestore
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Firebase initialization flag
_firebase_initialized = False

def initialize_firebase():
    """Initialize Firebase Admin SDK"""
    global _firebase_initialized
    
    if _firebase_initialized:
        return
    
    firebase_key_path = os.getenv("FIREBASE_KEY_PATH", "./firebase-key.json")
    
    if not os.path.exists(firebase_key_path):
        print(f"⚠️  Firebase key not found at {firebase_key_path}")
        print("   Firebase features will not be available")
        print("   See FIREBASE_SETUP.md for configuration instructions")
        return
    
    try:
        cred = credentials.Certificate(firebase_key_path)
        firebase_admin.initialize_app(cred)
        _firebase_initialized = True
        print("✓ Firebase initialized successfully")
    except Exception as e:
        print(f"⚠️  Firebase initialization failed: {e}")

def get_firestore_client():
    """Get Firestore client instance"""
    if not _firebase_initialized:
        raise RuntimeError("Firebase not initialized. Check FIREBASE_KEY_PATH.")
    return firestore.client()

def get_auth_client():
    """Get Firebase Auth client"""
    if not _firebase_initialized:
        raise RuntimeError("Firebase not initialized. Check FIREBASE_KEY_PATH.")
    return auth

def is_firebase_initialized():
    """Check if Firebase is initialized"""
    return _firebase_initialized
