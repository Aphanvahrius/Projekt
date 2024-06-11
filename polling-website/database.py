import psycopg2
from psycopg2.extras import RealDictCursor
from config import Config

def get_db_connection():
    """Establish and return a database connection."""
    conn = psycopg2.connect(
        host=Config.DB_HOST,
        port=Config.DB_PORT,
        database=Config.DB_NAME,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD
    )
    return conn

def init_db():
    """Initialize the database and create necessary tables."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
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
    )
    """)
    conn.commit()
    cursor.close()
    conn.close()

def insert_poll_response(age, gender, education, support, building_type, environment_importance, opinion, attachment):
    """Insert a poll response into the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO poll_responses (age, gender, education, support, building_type, environment_importance, opinion, attachment)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (age, gender, education, support, ','.join(building_type), environment_importance, opinion, attachment))
    conn.commit()
    cursor.close()
    conn.close()
