import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.db import init_db
from app.config import STORAGE_DIR
from app.routers import channels, videos, trends, settings, upload
from app.services.scheduler_service import SchedulerService

app = FastAPI(
    title="Sarıbay AI YouTube Automation Studio API",
    description="Sıfır Maliyet Tam Otomatik YouTube Kanal Kurulum, İçerik & Video Yönetim Sistemi",
    version="1.0.0"
)

# Enable CORS for Frontend UI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Storage directory for serving rendered videos, audio, images, thumbnails
app.mount("/storage", StaticFiles(directory=str(STORAGE_DIR)), name="storage")

# Include API Routers
app.include_router(channels.router)
app.include_router(videos.router)
app.include_router(trends.router)
app.include_router(settings.router)
app.include_router(upload.router)

@app.on_event("startup")
def startup_event():
    init_db()
    try:
        scheduler = SchedulerService()
        scheduler.start()
    except Exception as e:
        print(f"Scheduler startup info: {e}")

from fastapi.responses import RedirectResponse

@app.get("/")
def root_redirect():
    return RedirectResponse(url="http://localhost:5173/")

@app.get("/api/health")
def health_check():
    return {
        "status": "online",
        "system": "Sarıbay AI YouTube Automation Studio",
        "author": "Selahattin Sarıbay (Sarıbay Yazılım)",
        "zero_cost_mode": True
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
