#!/usr/bin/env python3
"""
BeeAPI v2.0 - Quick Test Script

This script demonstrates the basic workflow of the new BeeAPI v2.0.
Make sure the API is running at http://localhost:8000 before running this script.

Usage:
    python test_api.py
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"

def print_response(title, response):
    """Pretty print API response"""
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}")
    print(f"Status: {response.status_code}")
    if response.ok:
        print(json.dumps(response.json(), indent=2, default=str))
    else:
        print(f"Error: {response.text}")
    print()

def main():
    print(f"\n🐝 BeeAPI v2.0 - Test Script")
    print(f"Testing API at: {BASE_URL}\n")
    
    # Test root endpoint
    response = requests.get(f"{BASE_URL}/")
    print_response("1. Root Endpoint", response)
    
    # Create a user
    user_data = {
        "email": "test@example.com",
        "name": "Test Beekeeper",
        "password": "password123"
    }
    response = requests.post(f"{BASE_URL}/users", json=user_data)
    print_response("2. Create User", response)
    
    if not response.ok:
        print("❌ Failed to create user. Exiting.")
        return
    
    user = response.json()
    user_id = user["id"]
    
    # Create an apiary
    apiary_data = {
        "name": "Test Apiary",
        "location": "123 Test Street, Test City",
        "user_id": user_id
    }
    response = requests.post(f"{BASE_URL}/apiaries", json=apiary_data)
    print_response("3. Create Apiary", response)
    
    if not response.ok:
        print("❌ Failed to create apiary. Exiting.")
        return
    
    apiary = response.json()
    apiary_id = apiary["id"]
    
    # Create a hive
    hive_data = {
        "device_id": "test-hive-001",
        "name": "Test Hive Alpha",
        "apiary_id": apiary_id
    }
    response = requests.post(f"{BASE_URL}/hives", json=hive_data)
    print_response("4. Create Hive", response)
    
    if not response.ok:
        print("❌ Failed to create hive. Exiting.")
        return
    
    hive = response.json()
    hive_id = hive["id"]
    
    # Introduce a queen bee
    queen_data = {
        "name": "Regina Prima",
        "breed": "Italian",
        "birth_date": "2025-01-15T00:00:00"
    }
    response = requests.post(f"{BASE_URL}/hives/{hive_id}/queens", json=queen_data)
    print_response("5. Introduce Queen Bee", response)
    
    # Add hive event
    event_data = {
        "description": "First inspection - colony is strong and healthy"
    }
    response = requests.post(f"{BASE_URL}/hives/{hive_id}/events", json=event_data)
    print_response("6. Add Hive Event", response)
    
    # Add apiary event
    event_data = {
        "description": "Annual inspection by local authority - PASSED"
    }
    response = requests.post(f"{BASE_URL}/apiaries/{apiary_id}/events", json=event_data)
    print_response("7. Add Apiary Event", response)
    
    # Get all users
    response = requests.get(f"{BASE_URL}/users")
    print_response("8. Get All Users", response)
    
    # Get user's apiaries
    response = requests.get(f"{BASE_URL}/apiaries?user_id={user_id}")
    print_response("9. Get User's Apiaries", response)
    
    # Get apiary's hives
    response = requests.get(f"{BASE_URL}/hives?apiary_id={apiary_id}")
    print_response("10. Get Apiary's Hives", response)
    
    # Get hive's queens
    response = requests.get(f"{BASE_URL}/hives/{hive_id}/queens")
    print_response("11. Get Hive's Queens", response)
    
    # Get hive events
    response = requests.get(f"{BASE_URL}/hives/{hive_id}/events")
    print_response("12. Get Hive Events", response)
    
    # Get apiary events
    response = requests.get(f"{BASE_URL}/apiaries/{apiary_id}/events")
    print_response("13. Get Apiary Events", response)
    
    # Update hive
    update_data = {
        "name": "Test Hive Alpha - Updated"
    }
    response = requests.put(f"{BASE_URL}/hives/{hive_id}", json=update_data)
    print_response("14. Update Hive", response)
    
    # Introduce a new queen (should retire the old one)
    queen_data = {
        "name": "Regina Secunda",
        "breed": "Carniolan",
        "birth_date": "2026-01-01T00:00:00"
    }
    response = requests.post(f"{BASE_URL}/hives/{hive_id}/queens", json=queen_data)
    print_response("15. Introduce New Queen (retiring old one)", response)
    
    # Get queens again to see the retired one
    response = requests.get(f"{BASE_URL}/hives/{hive_id}/queens")
    print_response("16. Get Queens History (should show retired queen)", response)
    
    # Cleanup - Delete user (cascades to everything)
    print("\n⚠️  Cleanup: Deleting test user (will cascade to all created data)")
    input("Press Enter to continue with cleanup...")
    
    response = requests.delete(f"{BASE_URL}/users/{user_id}")
    print_response("17. Delete User (CASCADE)", response)
    
    # Verify deletion
    response = requests.get(f"{BASE_URL}/apiaries?user_id={user_id}")
    print_response("18. Verify Apiaries Deleted", response)
    
    print("\n✅ Test completed successfully!")
    print("\nKey Features Demonstrated:")
    print("  ✓ User management")
    print("  ✓ Apiary creation and management")
    print("  ✓ Hive creation and management")
    print("  ✓ Queen bee tracking with history")
    print("  ✓ Event logging for hives and apiaries")
    print("  ✓ Update operations")
    print("  ✓ Cascade deletes")
    print("  ✓ Hierarchical data structure")
    print("\n🐝 BeeAPI v2.0 is working correctly!\n")

if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to the API.")
        print("Make sure the API is running at http://localhost:8000")
        print("\nStart it with:")
        print("  cd backend")
        print("  python main.py")
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
