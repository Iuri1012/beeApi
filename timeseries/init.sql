-- TimescaleDB Database Schema for BeeAPI v2.0
-- This database stores ONLY time-series telemetry data

-- Initialize TimescaleDB extension
CREATE EXTENSION IF NOT EXISTS timescaledb;

-- ==================== TELEMETRY READINGS HYPERTABLE ====================
-- Note: device_id references hives.device_id in the PostgreSQL database
-- We don't enforce foreign key constraints across databases
CREATE TABLE IF NOT EXISTS readings (
    time TIMESTAMPTZ NOT NULL,
    device_id VARCHAR(255) NOT NULL,
    temperature DOUBLE PRECISION,
    humidity DOUBLE PRECISION,
    weight DOUBLE PRECISION,
    sound_level DOUBLE PRECISION
);

-- Convert to hypertable for optimized time-series queries
SELECT create_hypertable('readings', 'time', if_not_exists => TRUE);

-- ==================== INDEXES ====================
CREATE INDEX IF NOT EXISTS idx_readings_device_id_time ON readings (device_id, time DESC);
CREATE INDEX IF NOT EXISTS idx_readings_time ON readings (time DESC);

-- ==================== CONTINUOUS AGGREGATE FOR HOURLY AVERAGES ====================
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
    MIN(temperature) AS min_temperature,
    MAX(humidity) AS max_humidity,
    MIN(humidity) AS min_humidity,
    COUNT(*) AS reading_count
FROM readings
GROUP BY bucket, device_id;

-- Add refresh policy for continuous aggregate
SELECT add_continuous_aggregate_policy('readings_hourly',
    start_offset => INTERVAL '3 hours',
    end_offset => INTERVAL '1 hour',
    schedule_interval => INTERVAL '1 hour',
    if_not_exists => TRUE);

-- ==================== DATA RETENTION POLICY (OPTIONAL) ====================
-- Uncomment to automatically drop old data after 1 year
-- SELECT add_retention_policy('readings', INTERVAL '1 year', if_not_exists => TRUE);

-- Log initialization
DO $$
BEGIN
    RAISE NOTICE 'TimescaleDB initialized successfully';
    RAISE NOTICE 'Hypertable: readings (optimized for time-series data)';
    RAISE NOTICE 'Continuous aggregate: readings_hourly';
END $$;


