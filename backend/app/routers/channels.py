from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.db import get_db

router = APIRouter(prefix="/api/channels", tags=["channels"])

class ChannelCreate(BaseModel):
    id: str
    name: str
    niche: str
    language: str = "tr"
    voice: str = "tr-TR-EmelNeural"
    auto_pilot: int = 0
    post_frequency: str = "1_per_day"
    video_format: str = "shorts"

@router.get("")
def list_channels():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM channels ORDER BY created_at DESC")
    channels = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return channels

@router.post("")
def create_channel(channel: ChannelCreate):
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute("""
        INSERT INTO channels (id, name, niche, language, voice, auto_pilot, post_frequency, video_format)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (channel.id, channel.name, channel.niche, channel.language, channel.voice, channel.auto_pilot, channel.post_frequency, channel.video_format))
        conn.commit()
    except Exception as e:
        conn.close()
        raise HTTPException(status_code=400, detail=str(e))
    conn.close()
    return {"status": "created", "id": channel.id}

@router.put("/{channel_id}/autopilot")
def toggle_autopilot(channel_id: str, auto_pilot: int):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE channels SET auto_pilot = ? WHERE id = ?", (auto_pilot, channel_id))
    conn.commit()
    conn.close()
    return {"status": "updated", "channel_id": channel_id, "auto_pilot": auto_pilot}

@router.delete("/{channel_id}")
def delete_channel(channel_id: str):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM channels WHERE id = ?", (channel_id,))
    conn.commit()
    conn.close()
    return {"status": "deleted", "channel_id": channel_id}
