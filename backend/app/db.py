import sqlite3
import json
from pathlib import Path
from app.config import DB_PATH

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    
    # Channels Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS channels (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        niche TEXT NOT NULL,
        language TEXT DEFAULT 'tr',
        voice TEXT DEFAULT 'tr-TR-EmelNeural',
        auto_pilot INTEGER DEFAULT 0,
        post_frequency TEXT DEFAULT '1_per_day',
        video_format TEXT DEFAULT 'shorts', -- 'shorts' or 'longform'
        youtube_channel_id TEXT,
        oauth_connected INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # Videos Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS videos (
        id TEXT PRIMARY KEY,
        channel_id TEXT NOT NULL,
        title TEXT NOT NULL,
        description TEXT,
        tags TEXT,
        topic TEXT,
        niche TEXT,
        status TEXT DEFAULT 'draft', -- draft, generating, ready, rendering, rendered, publishing, published, failed
        format TEXT DEFAULT 'shorts',
        script_data TEXT, -- JSON breakdown of scenes, tts text, image prompts
        audio_path TEXT,
        video_path TEXT,
        thumbnail_path TEXT,
        youtube_video_id TEXT,
        published_at TIMESTAMP,
        error_message TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (channel_id) REFERENCES channels (id)
    );
    """)

    # Trends Cache Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS trend_cache (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        query TEXT NOT NULL,
        results_json TEXT NOT NULL,
        scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # System Settings Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS settings (
        key TEXT PRIMARY KEY,
        value TEXT NOT NULL
    );
    """)

    # Insert default channel if none exists
    cursor.execute("SELECT COUNT(*) FROM channels")
    if cursor.fetchone()[0] == 0:
        cursor.execute("""
        INSERT INTO channels (id, name, niche, language, voice, auto_pilot, post_frequency, video_format)
        VALUES ('ch_kids_main', 'Sevimli Masal Dünyası', 'kids_stories', 'tr', 'tr-TR-EmelNeural', 1, '1_per_day', 'shorts');
        """)
        cursor.execute("""
        INSERT INTO channels (id, name, niche, language, voice, auto_pilot, post_frequency, video_format)
        VALUES ('ch_tech_main', 'AI Teknoloji Rehberi', 'ai_tech_facts', 'tr', 'tr-TR-AhmetNeural', 0, '1_per_day', 'shorts');
        """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully!")
