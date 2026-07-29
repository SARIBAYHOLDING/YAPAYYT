import time
import json
import uuid
import random
from pathlib import Path
from typing import Dict, Any
from apscheduler.schedulers.background import BackgroundScheduler
from app.db import get_db
from app.config import AUDIO_DIR, IMAGES_DIR, VIDEOS_DIR, THUMBNAILS_DIR
from app.services.script_generator import ScriptGenerator
from app.services.tts_engine import generate_tts_sync
from app.services.image_generator import ImageGenerator
from app.services.stock_video_fetcher import StockVideoFetcher
from app.services.sfx_music_engine import SFXMusicEngine
from app.services.thumbnail_builder import ThumbnailBuilder
from app.services.video_renderer import VideoRenderer
from app.services.youtube_uploader import YouTubeUploader

# Global Real-Time Job Progress Tracker
JOB_PROGRESS: Dict[str, Dict[str, Any]] = {}

class SchedulerService:
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.script_gen = ScriptGenerator()
        self.image_gen = ImageGenerator()
        self.stock_fetcher = StockVideoFetcher()
        self.sfx_engine = SFXMusicEngine()
        self.thumbnail_builder = ThumbnailBuilder()
        self.renderer = VideoRenderer()
        self.uploader = YouTubeUploader()

    def start(self):
        # Run auto-pilot check every 60 minutes
        self.scheduler.add_job(self.check_autopilot_channels, 'interval', minutes=60, id='autopilot_job')
        self.scheduler.start()
        print("Auto-pilot Scheduler Started Successfully!")

    def check_autopilot_channels(self):
        print("Scheduler: Checking active channels for auto-pilot generation...")
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM channels WHERE auto_pilot = 1")
        channels = cursor.fetchall()
        conn.close()

        for ch in channels:
            ch_dict = dict(ch)
            print(f"Auto-pilot processing for channel: {ch_dict['name']}")
            try:
                self.generate_and_publish_for_channel(ch_dict['id'])
            except Exception as e:
                print(f"Error in auto-pilot for {ch_dict['name']}: {e}")

    def generate_and_publish_for_channel(self, channel_id: str, custom_topic: str = None, job_id: str = None) -> str:
        if not job_id:
            job_id = f"job_{uuid.uuid4().hex[:8]}"

        def update_progress(percent: int, step_desc: str):
            JOB_PROGRESS[job_id] = {
                "status": "in_progress",
                "progress_percent": percent,
                "current_step": step_desc,
                "video_id": None
            }

        update_progress(10, "1/6 - Gemini AI ile Viral Hook & SEO Senaryosu Üretiliyor...")

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM channels WHERE id = ?", (channel_id,))
        ch_row = cursor.fetchone()
        if not ch_row:
            conn.close()
            JOB_PROGRESS[job_id] = {"status": "failed", "progress_percent": 0, "error": "Kanal bulunamadı"}
            raise ValueError("Channel not found")
        
        ch = dict(ch_row)
        niche = ch.get("niche", "kids_stories")
        format_type = ch.get("video_format", "shorts")
        voice = ch.get("voice", "tr-TR-EmelNeural")

        if not custom_topic:
            topic_pool = {
                "kids_stories": [
                    "Sihirli Ormanın Kayıp Yıldızı", "Küçük Dinazor Dino ve Dev Karpuz", 
                    "Uçan Kedicik Minnoşun Rüyası", "Tavşan Pamuk Ve Dev Havuç Macerası",
                    "Rengarenk Balık Boncuğun Okyanus Gezisi"
                ],
                "ai_tech_facts": [
                    "İnsan Beynini Geçen Yapay Zeka Devrimi", "2030 Yılında Yaşamımızı Değiştirecek 5 Teknoloji",
                    "Kuantum Bilgisayarlar Nasıl Çalışır?", "Otonom Robotların Geleceği"
                ]
            }
            topics = topic_pool.get(niche, ["Harika Bir Yolculuk Hikayesi"])
            custom_topic = random.choice(topics)

        video_id = f"vid_{uuid.uuid4().hex[:8]}"

        # 1. Script Generation
        print(f"[{video_id}] Generating AI script for topic: {custom_topic}")
        script_data = self.script_gen.generate_script(custom_topic, niche=niche, format_type=format_type, language=ch.get("language", "tr"))

        cursor.execute("""
        INSERT INTO videos (id, channel_id, title, description, tags, topic, niche, status, format, script_data)
        VALUES (?, ?, ?, ?, ?, ?, ?, 'generating', ?, ?);
        """, (
            video_id, channel_id, script_data["title"], script_data["description"], 
            json.dumps(script_data["tags"]), custom_topic, niche, format_type, json.dumps(script_data)
        ))
        conn.commit()

        # 2. TTS Voiceover & Music Mix
        update_progress(30, "2/6 - Microsoft Edge Neural Speech ile Doğal Seslendirme Oluşturuluyor...")
        raw_audio_file = AUDIO_DIR / f"{video_id}_raw.mp3"
        mixed_audio_file = AUDIO_DIR / f"{video_id}.mp3"
        srt_file = AUDIO_DIR / f"{video_id}.srt"
        
        full_text = " ".join([s["narration"] for s in script_data["scenes"]])
        generate_tts_sync(full_text, str(raw_audio_file), voice=voice, output_srt_path=str(srt_file))

        update_progress(45, "3/6 - SFX Ses Efektleri & Arka Plan Müziği Miksleniyor...")
        self.sfx_engine.mix_narration_with_music(raw_audio_file, mixed_audio_file, mood=niche)

        # 3. Visuals Generation
        update_progress(60, "4/6 - Pollinations AI & HD Klipler Çekiliyor...")
        is_shorts = (format_type == "shorts")
        w, h = (1080, 1920) if is_shorts else (1920, 1080)
        
        scenes_with_images = []
        for i, sc in enumerate(script_data["scenes"]):
            img_path = IMAGES_DIR / f"{video_id}_scene_{i+1}.jpg"
            self.image_gen.generate_ai_image(sc["visual_prompt"], img_path, width=w, height=h, style_preset=niche)
            scenes_with_images.append({
                "scene_num": sc["scene_num"],
                "narration": sc["narration"],
                "image_path": str(img_path)
            })

        # 4. Thumbnail Builder
        update_progress(75, "5/6 - Yüksek CTR YouTube Kapak Görseli Tasarlanıyor...")
        thumb_path = THUMBNAILS_DIR / f"{video_id}_thumb.jpg"
        self.thumbnail_builder.create_thumbnail(
            Path(scenes_with_images[0]["image_path"]),
            script_data["title"],
            thumb_path,
            is_shorts=is_shorts
        )

        # 5. FFmpeg Video Render
        update_progress(88, "6/6 - FFmpeg 1080p Video İşleniyor (Render)...")
        rendered_mp4 = VIDEOS_DIR / f"{video_id}.mp4"
        self.renderer.render_video(
            scenes_with_images,
            mixed_audio_file,
            rendered_mp4,
            is_shorts=is_shorts,
            title=script_data["title"]
        )

        rel_audio = f"storage/audio/{mixed_audio_file.name}"
        rel_video = f"storage/videos/{rendered_mp4.name}"
        rel_thumb = f"storage/thumbnails/{thumb_path.name}"

        cursor.execute("""
        UPDATE videos 
        SET status = 'rendered', audio_path = ?, video_path = ?, thumbnail_path = ?
        WHERE id = ?;
        """, (rel_audio, rel_video, rel_thumb, video_id))
        conn.commit()

        # 6. YouTube Auto-Upload
        print(f"[{video_id}] Attempting YouTube auto-upload...")
        pub_result = self.uploader.upload_video(
            channel_id,
            rendered_mp4,
            script_data["title"],
            script_data["description"],
            script_data["tags"],
            thumbnail_path=thumb_path,
            is_kids=(niche in ["kids_stories", "kids_learning", "bedtime_tales"])
        )

        if pub_result.get("status") == "published":
            cursor.execute("UPDATE videos SET status = 'published', youtube_video_id = ? WHERE id = ?", (pub_result.get("youtube_video_id"), video_id))
        else:
            cursor.execute("UPDATE videos SET status = 'ready' WHERE id = ?", (video_id,))

        conn.commit()
        conn.close()

        JOB_PROGRESS[job_id] = {
            "status": "completed",
            "progress_percent": 100,
            "current_step": "🎉 Video ve Kapak Görseli Başarıyla Tamamlandı!",
            "video_id": video_id
        }

        return video_id

if __name__ == "__main__":
    svc = SchedulerService()
    print("SchedulerService module ready.")
