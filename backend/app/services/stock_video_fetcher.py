import os
import requests
import random
import urllib.parse
from pathlib import Path
from typing import Dict, Any, List
from app.config import STORAGE_DIR

CLIPS_DIR = STORAGE_DIR / "clips"
CLIPS_DIR.mkdir(parents=True, exist_ok=True)

class StockVideoFetcher:
    def __init__(self, pexels_key: str = None):
        self.pexels_key = pexels_key or os.environ.get("PEXELS_API_KEY", "")

    def fetch_video_clip(self, query: str, output_path: Path, is_shorts: bool = True) -> str:
        """
        Fetches a high quality 1080p MP4 video clip matching the query.
        Uses Pexels Video API or free open stock video mirrors.
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        if self.pexels_key:
            try:
                headers = {"Authorization": self.pexels_key}
                orientation = "portrait" if is_shorts else "landscape"
                url = f"https://api.pexels.com/videos/search?query={urllib.parse.quote(query)}&orientation={orientation}&per_page=5"
                res = requests.get(url, headers=headers, timeout=8)
                if res.status_code == 200:
                    data = res.json()
                    videos = data.get("videos", [])
                    if videos:
                        video_files = videos[0].get("video_files", [])
                        # Pick best HD 1080p file
                        hd_files = [f for f in video_files if f.get("width", 0) >= 720]
                        target_file = hd_files[0] if hd_files else video_files[0]
                        download_url = target_file.get("link")
                        
                        v_res = requests.get(download_url, stream=True, timeout=15)
                        if v_res.status_code == 200:
                            with open(output_path, "wb") as f:
                                for chunk in v_res.iter_content(chunk_size=1024*1024):
                                    f.write(chunk)
                            return str(output_path)
            except Exception as e:
                print(f"Pexels Video API warning: {e}")

        # Open Stock Video Fallback Sources (Free Pexels direct CDN clips)
        fallback_clips = {
            "nature": "https://videos.pexels.com/video-files/856973/856973-hd_1080_1920_30fps.mp4",
            "forest": "https://videos.pexels.com/video-files/1448735/1448735-hd_1080_1920_24fps.mp4",
            "magic": "https://videos.pexels.com/video-files/3129671/3129671-hd_1080_1920_30fps.mp4",
            "tech": "https://videos.pexels.com/video-files/3129957/3129957-hd_1080_1920_25fps.mp4",
            "space": "https://videos.pexels.com/video-files/856403/856403-hd_1080_1920_30fps.mp4"
        }

        chosen_key = "forest" if "forest" in query.lower() or "orman" in query.lower() else ("tech" if "tech" in query.lower() or "ai" in query.lower() else "magic")
        fallback_url = fallback_clips[chosen_key]

        try:
            r = requests.get(fallback_url, stream=True, timeout=10)
            if r.status_code == 200:
                with open(output_path, "wb") as f:
                    for chunk in r.iter_content(chunk_size=1024*1024):
                        f.write(chunk)
                return str(output_path)
        except Exception as e:
            print(f"Fallback clip download warning: {e}")

        return None

if __name__ == "__main__":
    fetcher = StockVideoFetcher()
    print("StockVideoFetcher module ready.")
