-- Initialize TimescaleDB extension
CREATE EXTENSION IF NOT EXISTS timescaledb;

-- Devices/Hives table
CREATE TABLE IF NOT EXISTS hives (
    id SERIAL PRIMARY KEY,
    device_id VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255),
    location VARCHAR(255),
    registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Telemetry readings hypertable
CREATE TABLE IF NOT EXISTS readings (
    time TIMESTAMPTZ NOT NULL,
    device_id VARCHAR(255) NOT NULL,
    temperature DOUBLE PRECISION,
    humidity DOUBLE PRECISION,
    weight DOUBLE PRECISION,
    sound_level DOUBLE PRECISION,
    FOREIGN KEY (device_id) REFERENCES hives(device_id) ON DELETE CASCADE
);

-- Convert to hypertable
SELECT create_hypertable('readings', 'time', if_not_exists => TRUE);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_readings_device_id_time ON readings (device_id, time DESC);
CREATE INDEX IF NOT EXISTS idx_hives_device_id ON hives (device_id);

-- Create continuous aggregate for hourly averages
CREATE MATERIALIZED VIEW IF NOT EXISTS readings_hourly
WITH (timescaledb.continuous) AS
SELECT
    time_bucket('1 hour', time) AS bucket,
    device_id,
    AVG(temperature) AS avg_temperature,
    AVG(humidity) AS avg_humidity,
    AVG(weight) AS avg_weight,
    AVG(sound_level) AS avg_sound_level,
    MAX(temperature) AS max_temperature,
    MIN(temperature) AS min_temperature
FROM readings
GROUP BY bucket, device_id;

-- Add refresh policy for continuous aggregate
SELECT add_continuous_aggregate_policy('readings_hourly',
    start_offset => INTERVAL '3 hours',
    end_offset => INTERVAL '1 hour',
    schedule_interval => INTERVAL '1 hour',
    if_not_exists => TRUE);

-- Insert sample hive for testing
INSERT INTO hives (device_id, name, location) 
VALUES ('hive-001', 'Test Hive Alpha', 'Apiary A')
ON CONFLICT (device_id) DO NOTHING;
