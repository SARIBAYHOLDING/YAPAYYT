from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict, Any
from app.db import get_db
from app.config import NICHES
from app.services.tts_engine import AVAILABLE_VOICES

router = APIRouter(prefix="/api/settings", tags=["settings"])

class SettingUpdate(BaseModel):
    key: str
    value: str

@router.get("")
def get_settings():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM settings")
    settings = {row["key"]: row["value"] for row in cursor.fetchall()}
    conn.close()
    return {
        "settings": settings,
        "niches": NICHES,
        "available_voices": AVAILABLE_VOICES
    }

@router.post("")
def update_setting(item: SettingUpdate):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)", (item.key, item.value))
    conn.commit()
    conn.close()
    return {"status": "success", "key": item.key, "value": item.value}
