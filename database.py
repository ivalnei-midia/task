import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id SERIAL PRIMARY KEY,
        description TEXT NOT NULL,
        completed BOOLEAN DEFAULT FALSE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        priority INTEGER DEFAULT 0,
        usuario TEXT DEFAULT ''
    )
    """)
    
    # Verificar se as colunas já existem e adicioná-las se não existirem
    cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name='tasks' AND column_name='priority'")
    if cursor.fetchone() is None:
        cursor.execute("ALTER TABLE tasks ADD COLUMN priority INTEGER DEFAULT 0")
    
    cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name='tasks' AND column_name='usuario'")
    if cursor.fetchone() is None:
        cursor.execute("ALTER TABLE tasks ADD COLUMN usuario TEXT DEFAULT ''")
    
    conn.commit()
    cursor.close()
    conn.close()