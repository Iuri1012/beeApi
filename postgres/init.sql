-- PostgreSQL Database Schema for BeeAPI v2.0
-- This database stores all relational/entity data
-- User authentication is handled by Firebase (user_id is Firebase UID)

-- ==================== APIARIES TABLE ====================
-- user_id is a VARCHAR that stores the Firebase UID
CREATE TABLE IF NOT EXISTS apiaries (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    location VARCHAR(255),
    user_id VARCHAR(255) NOT NULL,  -- Firebase UID
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP
);

-- ==================== HIVES TABLE ====================
CREATE TABLE IF NOT EXISTS hives (
    id SERIAL PRIMARY KEY,
    device_id VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255),
    apiary_id INTEGER NOT NULL,
    current_queen_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    FOREIGN KEY (apiary_id) REFERENCES apiaries(id) ON DELETE CASCADE
);

-- ==================== QUEEN BEES TABLE ====================
CREATE TABLE IF NOT EXISTS queen_bees (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    breed VARCHAR(255),
    birth_date TIMESTAMP,
    introduced_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    retired_date TIMESTAMP,
    hive_id INTEGER NOT NULL,
    FOREIGN KEY (hive_id) REFERENCES hives(id) ON DELETE CASCADE
);

-- Add foreign key constraint for current_queen_id (after queen_bees table is created)
ALTER TABLE hives 
    DROP CONSTRAINT IF EXISTS hives_current_queen_id_fkey,
    ADD CONSTRAINT hives_current_queen_id_fkey 
    FOREIGN KEY (current_queen_id) REFERENCES queen_bees(id) ON DELETE SET NULL;

-- ==================== EVENTS TABLE ====================
CREATE TABLE IF NOT EXISTS events (
    id SERIAL PRIMARY KEY,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    description TEXT NOT NULL,
    hive_id INTEGER,
    apiary_id INTEGER,
    FOREIGN KEY (hive_id) REFERENCES hives(id) ON DELETE CASCADE,
    FOREIGN KEY (apiary_id) REFERENCES apiaries(id) ON DELETE CASCADE,
    CHECK (
        (hive_id IS NOT NULL AND apiary_id IS NULL) OR 
        (hive_id IS NULL AND apiary_id IS NOT NULL)
    )
);

-- ==================== INDEXES ====================
CREATE INDEX IF NOT EXISTS idx_hives_device_id ON hives (device_id);
CREATE INDEX IF NOT EXISTS idx_hives_apiary_id ON hives (apiary_id);
CREATE INDEX IF NOT EXISTS idx_apiaries_user_id ON apiaries (user_id);
CREATE INDEX IF NOT EXISTS idx_queen_bees_hive_id ON queen_bees (hive_id);
CREATE INDEX IF NOT EXISTS idx_events_hive_id ON events (hive_id, date DESC);
CREATE INDEX IF NOT EXISTS idx_events_apiary_id ON events (apiary_id, date DESC);

-- ==================== SAMPLE DATA ====================
-- Note: Sample data uses a placeholder Firebase UID
-- In production, this would be a real Firebase UID from registration

-- Insert sample apiary with placeholder user_id
INSERT INTO apiaries (name, location, user_id) 
VALUES ('Demo Apiary', 'Demo Location', 'demo-user-uid-placeholder')
ON CONFLICT DO NOTHING;

-- Insert sample hive (only if apiary exists)
INSERT INTO hives (device_id, name, apiary_id) 
SELECT 'hive-demo-001', 'Demo Hive', id
FROM apiaries WHERE user_id = 'demo-user-uid-placeholder'
LIMIT 1
ON CONFLICT (device_id) DO NOTHING;

-- Log initialization
DO $$
BEGIN
    RAISE NOTICE 'PostgreSQL database initialized successfully';
    RAISE NOTICE 'User authentication handled by Firebase';
    RAISE NOTICE 'user_id columns store Firebase UIDs (VARCHAR)';
END $$;
