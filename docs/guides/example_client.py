#!/usr/bin/env python3
"""
Example: Programmatic interaction with BeeAPI

This script demonstrates how to:
1. Register a new device
2. Retrieve hive list
3. Get telemetry data
4. Connect to WebSocket for live updates
"""

import asyncio
import json
import requests
import websockets
from datetime import datetime


API_URL = "http://localhost:8000"
WS_URL = "ws://localhost:8000"


def register_device(device_id, name, location):
    """Register a new beehive device"""
    print(f"Registering device {device_id}...")
    
    response = requests.post(
        f"{API_URL}/register-device",
        json={
            "device_id": device_id,
            "name": name,
            "location": location
        }
    )
    
    if response.status_code == 200:
        print(f"✓ Device registered: {response.json()}")
        return response.json()
    else:
        print(f"✗ Registration failed: {response.text}")
        return None


def get_hives():
    """Get list of all registered hives"""
    print("Fetching hives...")
    
    response = requests.get(f"{API_URL}/hives")
    
    if response.status_code == 200:
        hives = response.json()
        print(f"✓ Found {len(hives)} hive(s)")
        for hive in hives:
            print(f"  - {hive['device_id']}: {hive['name']} @ {hive['location']}")
        return hives
    else:
        print(f"✗ Failed to get hives: {response.text}")
        return []


def get_telemetry(device_id, limit=10):
    """Get historical telemetry for a device"""
    print(f"Fetching telemetry for {device_id}...")
    
    response = requests.get(
        f"{API_URL}/hives/{device_id}/telemetry",
        params={"limit": limit}
    )
    
    if response.status_code == 200:
        readings = response.json()
        print(f"✓ Retrieved {len(readings)} reading(s)")
        
        if readings:
            latest = readings[-1]
            print(f"  Latest reading:")
            print(f"    Time: {latest['time']}")
            print(f"    Temperature: {latest['temperature']}°C")
            print(f"    Humidity: {latest['humidity']}%")
            print(f"    Weight: {latest['weight']}kg")
            print(f"    Sound: {latest['sound_level']}dB")
        
        return readings
    else:
        print(f"✗ Failed to get telemetry: {response.text}")
        return []


async def subscribe_to_telemetry(device_id, duration=30):
    """Subscribe to live telemetry via WebSocket"""
    print(f"Connecting to WebSocket for {device_id}...")
    print(f"Will listen for {duration} seconds...")
    
    uri = f"{WS_URL}/ws/hive/{device_id}/telemetry"
    
    try:
        async with websockets.connect(uri) as websocket:
            print("✓ WebSocket connected!")
            
            start_time = asyncio.get_event_loop().time()
            count = 0
            
            while True:
                # Check if duration exceeded
                if asyncio.get_event_loop().time() - start_time > duration:
                    print(f"\nReceived {count} telemetry messages")
                    break
                
                try:
                    # Wait for message with timeout
                    message = await asyncio.wait_for(
                        websocket.recv(),
                        timeout=5.0
                    )
                    
                    data = json.loads(message)
                    
                    # Skip ping messages
                    if data.get('type') == 'ping':
                        continue
                    
                    count += 1
                    print(f"\n[{count}] Telemetry received:")
                    print(f"  Time: {data.get('time')}")
                    print(f"  Temp: {data.get('temperature')}°C")
                    print(f"  Humidity: {data.get('humidity')}%")
                    print(f"  Weight: {data.get('weight')}kg")
                    print(f"  Sound: {data.get('sound_level')}dB")
                    
                except asyncio.TimeoutError:
                    # No message received in timeout period
                    print(".", end="", flush=True)
                    continue
                    
    except Exception as e:
        print(f"✗ WebSocket error: {e}")


def main():
    print("=" * 60)
    print("BeeAPI Example Client")
    print("=" * 60)
    print()
    
    # Check API is available
    try:
        response = requests.get(f"{API_URL}/")
        print(f"✓ API is available: {response.json()['message']}")
        print()
    except Exception as e:
        print(f"✗ Cannot connect to API at {API_URL}")
        print(f"  Make sure services are running: ./scripts/run_local.sh")
        return
    
    # Get existing hives
    hives = get_hives()
    print()
    
    # If no hives, register one
    if not hives:
        print("No hives found. Registering example hive...")
        register_device("example-hive-001", "Example Hive", "Example Location")
        print()
        hives = get_hives()
        print()
    
    # Get telemetry for first hive
    if hives:
        device_id = hives[0]['device_id']
        get_telemetry(device_id, limit=5)
        print()
        
        # Subscribe to live updates
        print("To subscribe to live telemetry, run:")
        print(f"  python3 -c 'import asyncio; from {__file__} import subscribe_to_telemetry; asyncio.run(subscribe_to_telemetry(\"{device_id}\", 30))'")
        print()
        print("Or uncomment the line below and run the script again:")
        print()
        # Uncomment to enable live telemetry subscription:
        # asyncio.run(subscribe_to_telemetry(device_id, duration=30))
    
    print("=" * 60)
    print("Example complete!")
    print("=" * 60)


if __name__ == '__main__':
    main()
