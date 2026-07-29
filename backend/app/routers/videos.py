from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import json
import uuid
from pathlib import Path
from app.db import get_db
from app.services.scheduler_service import SchedulerService
from app.config import VIDEOS_DIR, AUDIO_DIR, THUMBNAILS_DIR

router = APIRouter(prefix="/api/videos", tags=["videos"])
scheduler_service = SchedulerService()

class GenerateVideoRequest(BaseModel):
    channel_id: str
    topic: str
    niche: Optional[str] = "kids_stories"
    format: Optional[str] = "shorts"
    voice: Optional[str] = "tr-TR-EmelNeural"

@router.get("")
def list_videos(channel_id: Optional[str] = None):
    conn = get_db()
    cursor = conn.cursor()
    if channel_id:
        cursor.execute("SELECT * FROM videos WHERE channel_id = ? ORDER BY created_at DESC", (channel_id,))
    else:
        cursor.execute("SELECT * FROM videos ORDER BY created_at DESC")
    
    videos = []
    for row in cursor.fetchall():
        v = dict(row)
        if v.get("script_data"):
            try:
                v["script_data"] = json.loads(v["script_data"])
            except Exception:
                pass
        videos.append(v)
    conn.close()
    return videos

@router.get("/{video_id}")
def get_video(video_id: str):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM videos WHERE id = ?", (video_id,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Video not found")
    v = dict(row)
    if v.get("script_data"):
        try:
            v["script_data"] = json.loads(v["script_data"])
        except Exception:
            pass
    return v

@router.post("/generate")
def generate_video(req: GenerateVideoRequest, background_tasks: BackgroundTasks):
    try:
        video_id = scheduler_service.generate_and_publish_for_channel(req.channel_id, req.topic)
        return {"status": "success", "video_id": video_id, "message": "Video generation and pipeline completed!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class BatchGenerateRequest(BaseModel):
    channel_id: str
    topics: List[str]
    niche: Optional[str] = "kids_stories"
    format: Optional[str] = "shorts"

@router.post("/batch-generate")
def batch_generate_videos(req: BatchGenerateRequest, background_tasks: BackgroundTasks):
    generated_ids = []
    for topic in req.topics:
        try:
            vid_id = scheduler_service.generate_and_publish_for_channel(req.channel_id, topic)
            generated_ids.append(vid_id)
        except Exception as e:
            print(f"Batch generation error for {topic}: {e}")
    return {"status": "success", "count": len(generated_ids), "video_ids": generated_ids}

@router.delete("/{video_id}")
def delete_video(video_id: str):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM videos WHERE id = ?", (video_id,))
    conn.commit()
    conn.close()
    return {"status": "deleted", "video_id": video_id}
