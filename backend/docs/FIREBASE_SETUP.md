# Firebase Setup Guide for BeeAPI

This guide explains how to configure Firebase Authentication for the BeeAPI backend.

## Overview

BeeAPI uses a hybrid database architecture:
- **Firebase Authentication + Firestore**: User accounts and profiles
- **PostgreSQL**: Entity data (apiaries, hives, queens, events)
- **TimescaleDB**: Time-series telemetry data

## Prerequisites

1. A Google Cloud/Firebase account
2. A Firebase project created at [Firebase Console](https://console.firebase.google.com/)

## Step 1: Create a Firebase Project

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Click "Add project"
3. Enter a project name (e.g., "BeeAPI")
4. Follow the setup wizard

## Step 2: Enable Authentication

1. In your Firebase project, go to **Build > Authentication**
2. Click "Get Started"
3. Enable **Email/Password** sign-in method
4. Optionally enable other methods (Google, etc.)

## Step 3: Enable Firestore

1. Go to **Build > Firestore Database**
2. Click "Create database"
3. Choose **Start in production mode**
4. Select a location close to your users

## Step 4: Generate Service Account Key

1. Go to **Project Settings** (gear icon) > **Service accounts**
2. Click **Generate new private key**
3. Save the downloaded JSON file as `firebase-key.json`
4. Place it in the `backend/` directory

## Step 5: Configure Security Rules

### Firestore Rules

Go to **Firestore Database > Rules** and add:

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Users collection
    match /users/{userId} {
      // Users can only read/write their own profile
      allow read, write: if request.auth != null && request.auth.uid == userId;
    }
  }
}
```

## Step 6: Environment Setup

Create a `.env` file in the `backend/` directory (optional):

```env
# Firebase (uses firebase-key.json by default)
FIREBASE_KEY_PATH=firebase-key.json

# PostgreSQL
POSTGRES_URL=postgresql://beeapi:beeapi123@localhost:5432/beeapi

# TimescaleDB
TIMESCALE_URL=postgresql://beeapi:beeapi123@localhost:5433/beeapi_telemetry
```

## File Structure

After setup, your `backend/` directory should look like:

```
backend/
├── firebase-key.json     # ⚠️ NEVER commit to git!
├── .env                  # Optional environment variables
├── main.py
├── config/
│   ├── __init__.py
│   └── firebase_config.py
├── middleware/
│   ├── __init__.py
│   └── auth.py
├── controllers/
│   ├── __init__.py
│   ├── user_controller.py    # Uses Firebase
│   └── bee_controller.py     # Uses PostgreSQL
└── models/
    ├── __init__.py
    ├── user_models.py
    └── bee_models.py
```

## Security Checklist

- [ ] `firebase-key.json` is in `.gitignore`
- [ ] Firestore security rules are configured
- [ ] Firebase Authentication is enabled
- [ ] Production mode is enabled for Firestore

## API Authentication Flow

### 1. Register a New User

```bash
curl -X POST http://localhost:8000/users/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword123",
    "name": "John Doe"
  }'
```

Response:
```json
{
  "access_token": "eyJhbGc...",
  "token_type": "bearer",
  "user_id": "abc123xyz",
  "email": "user@example.com"
}
```

### 2. Login (Client-Side Recommended)

For full authentication flow, use Firebase Client SDK:

**JavaScript:**
```javascript
import { signInWithEmailAndPassword } from "firebase/auth";

const userCredential = await signInWithEmailAndPassword(auth, email, password);
const idToken = await userCredential.user.getIdToken();
```

**Python:**
```python
import requests

# Use Firebase REST API
url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={API_KEY}"
response = requests.post(url, json={
    "email": email,
    "password": password,
    "returnSecureToken": True
})
id_token = response.json()["idToken"]
```

### 3. Use Token for Protected Endpoints

```bash
curl http://localhost:8000/apiaries \
  -H "Authorization: Bearer YOUR_FIREBASE_ID_TOKEN"
```

## Troubleshooting

### Firebase Not Initializing

1. Check `firebase-key.json` exists in `backend/`
2. Verify the JSON is valid
3. Check console output for errors

### 503 Service Unavailable

Firebase is not configured. Check:
1. `firebase-key.json` location
2. File permissions
3. JSON validity

### 401 Unauthorized

1. Token may be expired (Firebase tokens expire after 1 hour)
2. Token format is incorrect
3. Token wasn't issued by your Firebase project

## Testing Without Firebase

If you don't have Firebase configured:

1. The API will start but show warnings
2. `/users/*` endpoints will return 503 errors
3. Other endpoints requiring auth will return 401 errors
4. `/health` endpoint will show Firebase status

To test without authentication:
1. Temporarily remove `Depends(get_current_user_id)` from endpoints
2. Pass a hardcoded `user_id` for testing
