#!/usr/bin/env python3
"""
Integration test for BeeAPI components
Tests the simulator, backend API logic, and telemetry consumer logic
"""

import sys
import json
from datetime import datetime


def test_simulator_telemetry_generation():
    """Test that the simulator can generate valid telemetry"""
    print("Testing firmware simulator...")
    
    sys.path.insert(0, 'firmware')
    from simulator import BeehiveSimulator
    
    sim = BeehiveSimulator(device_id='test-hive-001')
    telemetry = sim.generate_telemetry()
    
    # Validate telemetry structure
    assert 'device_id' in telemetry, "Missing device_id"
    assert 'timestamp' in telemetry, "Missing timestamp"
    assert 'temperature' in telemetry, "Missing temperature"
    assert 'humidity' in telemetry, "Missing humidity"
    assert 'weight' in telemetry, "Missing weight"
    assert 'sound_level' in telemetry, "Missing sound_level"
    
    # Validate data types and ranges
    assert isinstance(telemetry['temperature'], (int, float)), "Temperature should be numeric"
    assert isinstance(telemetry['humidity'], (int, float)), "Humidity should be numeric"
    assert isinstance(telemetry['weight'], (int, float)), "Weight should be numeric"
    assert isinstance(telemetry['sound_level'], (int, float)), "Sound level should be numeric"
    
    # Validate ranges (realistic beehive values)
    assert 20 < telemetry['temperature'] < 50, "Temperature out of realistic range"
    assert 0 < telemetry['humidity'] < 100, "Humidity out of realistic range"
    assert telemetry['weight'] > 0, "Weight should be positive"
    assert telemetry['sound_level'] > 0, "Sound level should be positive"
    
    print(f"  ✓ Generated telemetry: {json.dumps(telemetry, indent=2)}")
    print("  ✓ All validations passed")
    return True


def test_backend_models():
    """Test that backend models are valid"""
    print("\nTesting backend models...")
    
    sys.path.insert(0, 'backend')
    from main import DeviceRegistration, Hive, TelemetryReading
    
    # Test device registration model
    device = DeviceRegistration(
        device_id="test-001",
        name="Test Hive",
        location="Test Location"
    )
    assert device.device_id == "test-001"
    print("  ✓ DeviceRegistration model works")
    
    # Test hive model
    hive = Hive(
        id=1,
        device_id="test-001",
        name="Test Hive",
        location="Test Location",
        registered_at=datetime.now()
    )
    assert hive.id == 1
    print("  ✓ Hive model works")
    
    # Test telemetry reading model
    reading = TelemetryReading(
        time=datetime.now(),
        device_id="test-001",
        temperature=35.5,
        humidity=62.0,
        weight=45.0,
        sound_level=50.0
    )
    assert reading.temperature == 35.5
    print("  ✓ TelemetryReading model works")
    
    return True


def test_sql_schema():
    """Test that SQL schema is valid"""
    print("\nTesting SQL schema...")
    
    with open('timeseries/init.sql', 'r') as f:
        sql = f.read()
    
    # Check for key statements
    assert 'CREATE EXTENSION IF NOT EXISTS timescaledb' in sql, "Missing TimescaleDB extension"
    assert 'CREATE TABLE IF NOT EXISTS hives' in sql, "Missing hives table"
    assert 'CREATE TABLE IF NOT EXISTS readings' in sql, "Missing readings table"
    assert 'create_hypertable' in sql, "Missing hypertable creation"
    assert 'CREATE INDEX' in sql, "Missing indexes"
    
    print("  ✓ SQL schema contains all required elements")
    return True


def test_docker_compose():
    """Test that docker-compose.yml is valid"""
    print("\nTesting docker-compose configuration...")
    
    import yaml
    
    with open('docker-compose.yml', 'r') as f:
        config = yaml.safe_load(f)
    
    # Check for required services
    required_services = ['mosquitto', 'postgres', 'backend', 'telemetry', 'web']
    services = config.get('services', {})
    
    for service in required_services:
        assert service in services, f"Missing service: {service}"
        print(f"  ✓ Service '{service}' defined")
    
    # Check postgres has TimescaleDB image
    assert 'timescale' in services['postgres']['image'], "Postgres should use TimescaleDB image"
    print("  ✓ PostgreSQL using TimescaleDB image")
    
    # Check backend has correct environment
    backend_env = services['backend'].get('environment', {})
    assert 'DATABASE_URL' in backend_env, "Backend missing DATABASE_URL"
    assert 'MQTT_BROKER' in backend_env, "Backend missing MQTT_BROKER"
    print("  ✓ Backend environment configured")
    
    return True


def main():
    print("=" * 60)
    print("BeeAPI Integration Tests")
    print("=" * 60)
    
    tests = [
        test_simulator_telemetry_generation,
        test_backend_models,
        test_sql_schema,
        test_docker_compose,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"  ✗ Test failed: {e}")
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 60)
    
    return 0 if failed == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
