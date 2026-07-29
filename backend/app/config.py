import os
from pathlib import Path

# Base Paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent
STORAGE_DIR = BASE_DIR / "storage"
AUDIO_DIR = STORAGE_DIR / "audio"
IMAGES_DIR = STORAGE_DIR / "images"
VIDEOS_DIR = STORAGE_DIR / "videos"
THUMBNAILS_DIR = STORAGE_DIR / "thumbnails"
TEMP_DIR = STORAGE_DIR / "temp"

for d in [STORAGE_DIR, AUDIO_DIR, IMAGES_DIR, VIDEOS_DIR, THUMBNAILS_DIR, TEMP_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# Database
DB_PATH = STORAGE_DIR / "youtube_studio.db"

# API Keys & Secrets (Loaded from Env or DB settings)
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
PEXELS_API_KEY = os.environ.get("PEXELS_API_KEY", "")
PIXABAY_API_KEY = os.environ.get("PIXABAY_API_KEY", "")

# YouTube Credentials
CLIENT_SECRETS_FILE = STORAGE_DIR / "client_secrets.json"
OAUTH_TOKENS_DIR = STORAGE_DIR / "tokens"
OAUTH_TOKENS_DIR.mkdir(parents=True, exist_ok=True)

# Default Niche Configurations & Voice Settings
NICHES = {
    "kids_stories": {
        "name": "Çocuk Hikayeleri & Masallar",
        "description": "Eğitici, sevimli, renkli animasyon masalları ve maceraları",
        "target_audience": "Children 3-10, Parents",
        "default_voice": "tr-TR-EmelNeural",
        "visual_style": "3d pixar disney style animated cute vibrant colorful illustration",
        "tone": "Warm, playful, whimsical, enthusiastic, storytelling"
    },
    "kids_learning": {
        "name": "Çocuklar İçin Öğretici (Renkler, Hayvanlar, Sayılar)",
        "description": "Okul öncesi eğlenceli ve interaktif öğrenme içerikleri",
        "target_audience": "Toddlers, Kids 2-6",
        "default_voice": "tr-TR-AhmetNeural",
        "visual_style": "bright vivid 3D cartoon, cheerful cute playful background",
        "tone": "Energetic, clear, repetitive learning, fun"
    },
    "bedtime_tales": {
        "name": "Sakinleştirici Uyku Masalları",
        "description": "Gece uyku öncesi dinlendirici masallar ve rahatlatıcı sesler",
        "target_audience": "Kids, Parents, General",
        "default_voice": "tr-TR-EmelNeural",
        "visual_style": "soft cozy starry night, magical dreamy fantasy fairytale digital art",
        "tone": "Calm, soothing, slow pace, soft whispers, peaceful"
    },
    "ai_tech_facts": {
        "name": "Yapay Zeka & Teknoloji İlginç Bilgiler",
        "description": "Geleceğin teknolojisi, bilim ve inanılmaz gerçekler",
        "target_audience": "Teens, Adults, Tech Enthusiasts",
        "default_voice": "tr-TR-AhmetNeural",
        "visual_style": "futuristic neon cyber tech, cinematic 8k ultra detailed hyperrealistic photorealistic",
        "tone": "Captivating, fast-paced, intriguing, mysterious, impactful"
    },
    "facts_mysteries": {
        "name": "İnanılmaz Bilgiler & Gizemler",
        "description": "Dünyadan ve evrenden duymadığınız en garip 5 bilgi",
        "target_audience": "General YouTube Audience",
        "default_voice": "tr-TR-AhmetNeural",
        "visual_style": "dramatic cinematic atmospheric dark mystery high contrast photorealistic",
        "tone": "Suspenseful, hooks first 3 seconds, curious, surprising"
    }
}
