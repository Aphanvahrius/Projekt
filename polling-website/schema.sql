CREATE TABLE IF NOT EXISTS poll_responses (
    id SERIAL PRIMARY KEY,
    age INTEGER NOT NULL,
    gender VARCHAR(10) NOT NULL,
    education VARCHAR(50) NOT NULL,
    support VARCHAR(3) NOT NULL,
    building_type VARCHAR(100) NOT NULL,
    environment_importance VARCHAR(50) NOT NULL,
    opinion TEXT,
    attachment VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
