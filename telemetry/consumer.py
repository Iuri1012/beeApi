#!/usr/bin/env python3
"""
Telemetry Consumer Service
Subscribes to MQTT telemetry messages and stores them in TimescaleDB
"""

import json
import os
import asyncio
from datetime import datetime
import paho.mqtt.client as mqtt
import asyncpg


class TelemetryConsumer:
    def __init__(self):
        self.mqtt_broker = os.getenv("MQTT_BROKER", "localhost")
        self.mqtt_port = int(os.getenv("MQTT_PORT", 1883))
        self.database_url = os.getenv("DATABASE_URL", "postgresql://beeapi:beeapi123@localhost:5432/beeapi")
        self.db_pool = None
        self.mqtt_client = mqtt.Client(client_id="telemetry_consumer")
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_message = self.on_message
        
    async def init_db(self):
        """Initialize database connection pool"""
        self.db_pool = await asyncpg.create_pool(
            self.database_url,
            min_size=2,
            max_size=10
        )
        print("Database connection pool created")
    
    def on_connect(self, client, userdata, flags, rc):
        """Callback when connected to MQTT broker"""
        if rc == 0:
            print(f"Connected to MQTT broker at {self.mqtt_broker}:{self.mqtt_port}")
            # Subscribe to all beehive telemetry topics
            client.subscribe("beehive/+/telemetry")
            print("Subscribed to beehive/+/telemetry")
        else:
            print(f"Connection failed with code {rc}")
    
    def on_message(self, client, userdata, msg):
        """Callback when MQTT message received"""
        try:
            payload = json.loads(msg.payload.decode())
            print(f"Received telemetry: {payload}")
            
            # Schedule the async database insert
            asyncio.create_task(self.store_telemetry(payload))
            
        except json.JSONDecodeError as e:
            print(f"Invalid JSON in message: {e}")
        except Exception as e:
            print(f"Error processing message: {e}")
    
    async def store_telemetry(self, telemetry):
        """Store telemetry data in database"""
        try:
            async with self.db_pool.acquire() as conn:
                # Ensure the device exists
                device_exists = await conn.fetchval(
                    "SELECT EXISTS(SELECT 1 FROM hives WHERE device_id = $1)",
                    telemetry['device_id']
                )
                
                if not device_exists:
                    print(f"Warning: Device {telemetry['device_id']} not registered. Skipping.")
                    return
                
                # Parse timestamp
                timestamp = telemetry.get('timestamp')
                if timestamp:
                    # Handle ISO format with Z
                    timestamp = timestamp.replace('Z', '+00:00')
                    time = datetime.fromisoformat(timestamp)
                else:
                    time = datetime.utcnow()
                
                # Insert telemetry reading
                await conn.execute(
                    """
                    INSERT INTO readings (time, device_id, temperature, humidity, weight, sound_level)
                    VALUES ($1, $2, $3, $4, $5, $6)
                    """,
                    time,
                    telemetry['device_id'],
                    telemetry.get('temperature'),
                    telemetry.get('humidity'),
                    telemetry.get('weight'),
                    telemetry.get('sound_level')
                )
                
                print(f"Stored telemetry for {telemetry['device_id']} at {time}")
                
        except Exception as e:
            print(f"Error storing telemetry: {e}")
    
    async def run(self):
        """Run the telemetry consumer"""
        # Initialize database
        await self.init_db()
        
        # Connect to MQTT broker
        print(f"Connecting to MQTT broker at {self.mqtt_broker}:{self.mqtt_port}...")
        self.mqtt_client.connect(self.mqtt_broker, self.mqtt_port, 60)
        
        # Start MQTT loop in background thread
        self.mqtt_client.loop_start()
        
        print("Telemetry consumer running. Press Ctrl+C to stop.")
        
        try:
            # Keep the service running
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            print("\nStopping telemetry consumer...")
        finally:
            self.mqtt_client.loop_stop()
            self.mqtt_client.disconnect()
            if self.db_pool:
                await self.db_pool.close()
            print("Telemetry consumer stopped")


async def main():
    consumer = TelemetryConsumer()
    await consumer.run()


if __name__ == '__main__':
    asyncio.run(main())
