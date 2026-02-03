#!/usr/bin/env python3
"""
Beehive Firmware Simulator
Simulates a beehive device that publishes telemetry data via MQTT
"""

import json
import random
import time
import argparse
from datetime import datetime
import paho.mqtt.client as mqtt


class BeehiveSimulator:
    def __init__(self, device_id, broker_host='localhost', broker_port=1883):
        self.device_id = device_id
        self.broker_host = broker_host
        self.broker_port = broker_port
        self.client = mqtt.Client(client_id=f"simulator_{device_id}")
        self.topic = f"beehive/{device_id}/telemetry"
        
        # Simulated baseline values with some variation
        self.base_temperature = 35.0  # Celsius
        self.base_humidity = 60.0     # Percentage
        self.base_weight = 45.0       # Kilograms
        self.base_sound = 50.0        # Decibels
        
    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print(f"[{self.device_id}] Connected to MQTT broker at {self.broker_host}:{self.broker_port}")
        else:
            print(f"[{self.device_id}] Connection failed with code {rc}")
    
    def on_publish(self, client, userdata, mid):
        print(f"[{self.device_id}] Message published (mid: {mid})")
    
    def generate_telemetry(self):
        """Generate realistic beehive telemetry data"""
        # Add random variations to simulate real conditions
        temperature = self.base_temperature + random.uniform(-2.0, 2.0)
        humidity = self.base_humidity + random.uniform(-5.0, 5.0)
        weight = self.base_weight + random.uniform(-0.5, 0.5)
        sound_level = self.base_sound + random.uniform(-10.0, 10.0)
        
        telemetry = {
            "device_id": self.device_id,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "temperature": round(temperature, 2),
            "humidity": round(humidity, 2),
            "weight": round(weight, 2),
            "sound_level": round(sound_level, 2)
        }
        return telemetry
    
    def connect(self):
        """Connect to MQTT broker"""
        self.client.on_connect = self.on_connect
        self.client.on_publish = self.on_publish
        
        try:
            self.client.connect(self.broker_host, self.broker_port, 60)
            self.client.loop_start()
            time.sleep(1)  # Wait for connection
            return True
        except Exception as e:
            print(f"[{self.device_id}] Error connecting: {e}")
            return False
    
    def publish_telemetry(self):
        """Generate and publish telemetry data"""
        telemetry = self.generate_telemetry()
        payload = json.dumps(telemetry)
        
        result = self.client.publish(self.topic, payload, qos=1)
        
        if result.rc == mqtt.MQTT_ERR_SUCCESS:
            print(f"[{self.device_id}] Published: {payload}")
        else:
            print(f"[{self.device_id}] Publish failed with code {result.rc}")
        
        return result.rc == mqtt.MQTT_ERR_SUCCESS
    
    def run(self, interval=5, count=None):
        """
        Run the simulator
        
        Args:
            interval: Seconds between telemetry transmissions
            count: Number of messages to send (None for infinite)
        """
        if not self.connect():
            print(f"[{self.device_id}] Failed to connect. Exiting.")
            return
        
        print(f"[{self.device_id}] Starting telemetry transmission (interval: {interval}s)")
        
        messages_sent = 0
        try:
            while count is None or messages_sent < count:
                self.publish_telemetry()
                messages_sent += 1
                time.sleep(interval)
        except KeyboardInterrupt:
            print(f"\n[{self.device_id}] Stopped by user")
        finally:
            self.client.loop_stop()
            self.client.disconnect()
            print(f"[{self.device_id}] Disconnected. Total messages sent: {messages_sent}")


def main():
    parser = argparse.ArgumentParser(description='Beehive Firmware Simulator')
    parser.add_argument('--device-id', default='hive-001', 
                        help='Device ID (default: hive-001)')
    parser.add_argument('--broker', default='localhost',
                        help='MQTT broker host (default: localhost)')
    parser.add_argument('--port', type=int, default=1883,
                        help='MQTT broker port (default: 1883)')
    parser.add_argument('--interval', type=int, default=5,
                        help='Seconds between transmissions (default: 5)')
    parser.add_argument('--count', type=int, default=None,
                        help='Number of messages to send (default: infinite)')
    
    args = parser.parse_args()
    
    simulator = BeehiveSimulator(
        device_id=args.device_id,
        broker_host=args.broker,
        broker_port=args.port
    )
    
    simulator.run(interval=args.interval, count=args.count)


if __name__ == '__main__':
    main()
