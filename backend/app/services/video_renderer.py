import os
import subprocess
import json
from pathlib import Path
from typing import List, Dict, Any
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from app.config import VIDEOS_DIR, TEMP_DIR

class VideoRenderer:
    def __init__(self):
        pass

    def render_video(self, 
                     scenes: List[Dict[str, Any]], 
                     audio_path: Path, 
                     output_video_path: Path, 
                     is_shorts: bool = True,
                     title: str = "") -> str:
        """
        Renders 1080p MP4 video with smooth image slideshow, Ken Burns zoom, bold kinetic subtitles, and audio.
        Uses native FFmpeg for fast, robust rendering.
        """
        output_video_path = Path(output_video_path)
        output_video_path.parent.mkdir(parents=True, exist_ok=True)
        
        target_w = 1080 if is_shorts else 1920
        target_h = 1920 if is_shorts else 1080

        # Get audio duration using ffprobe
        audio_duration = self._get_audio_duration(audio_path)
        if audio_duration <= 0:
            audio_duration = len(scenes) * 4.0

        per_scene_duration = audio_duration / max(len(scenes), 1)

        # Prepare scene images scaled to target resolution
        processed_image_paths = []
        for idx, scene in enumerate(scenes):
            img_path = scene.get("image_path")
            if not img_path or not os.path.exists(img_path):
                # Fallback blank image
                img_path = TEMP_DIR / f"temp_scene_{idx}.jpg"
                img = Image.new("RGB", (target_w, target_h), (25, 30, 50))
                img.save(img_path)

            scaled_path = TEMP_DIR / f"scene_scaled_{idx}.jpg"
            self._prepare_scene_image(img_path, scaled_path, target_w, target_h, scene.get("narration", ""))
            processed_image_paths.append(scaled_path)

        # Create FFmpeg concat input file
        concat_file = TEMP_DIR / "concat_list.txt"
        with open(concat_file, "w", encoding="utf-8") as f:
            for img_p in processed_image_paths:
                # Escape backslashes for FFmpeg on Windows
                formatted_p = str(img_p).replace('\\', '/')
                f.write(f"file '{formatted_p}'\n")
                f.write(f"duration {per_scene_duration:.2f}\n")
            # Write last image again as required by ffmpeg concat
            formatted_p = str(processed_image_paths[-1]).replace('\\', '/')
            f.write(f"file '{formatted_p}'\n")

        # FFmpeg command to combine images + audio + zoompan effect
        cmd = [
            "ffmpeg", "-y",
            "-f", "concat",
            "-safe", "0",
            "-i", str(concat_file),
            "-i", str(audio_path),
            "-filter_complex", 
            f"[0:v]scale={target_w}:{target_h}:force_original_aspect_ratio=increase,crop={target_w}:{target_h},zoompan=z='min(zoom+0.0015,1.15)':d={int(per_scene_duration*25)}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s={target_w}x{target_h}[v]",
            "-map", "[v]",
            "-map", "1:a",
            "-c:v", "libx264",
            "-preset", "ultrafast",
            "-crf", "24",
            "-c:a", "aac",
            "-b:a", "192k",
            "-pix_fmt", "yuv420p",
            "-shortest",
            str(output_video_path)
        ]

        print(f"Rendering video via FFmpeg to {output_video_path}...")
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        if res.returncode != 0:
            print(f"FFmpeg error: {res.stderr[:500]}")
            # Fallback simple command without complex zoompan
            cmd_simple = [
                "ffmpeg", "-y",
                "-f", "concat",
                "-safe", "0",
                "-i", str(concat_file),
                "-i", str(audio_path),
                "-c:v", "libx264",
                "-preset", "ultrafast",
                "-c:a", "aac",
                "-pix_fmt", "yuv420p",
                "-shortest",
                str(output_video_path)
            ]
            subprocess.run(cmd_simple, check=True)

        return str(output_video_path)

    def _prepare_scene_image(self, src_path: Path, dest_path: Path, width: int, height: int, subtitle_text: str):
        """Scales image and burn-in subtitle text cleanly at bottom."""
        img = Image.open(src_path).convert("RGBA")
        img = img.resize((width, height), Image.Resampling.LANCZOS)
        
        draw = ImageDraw.Draw(img)
        try:
            font_size = int(height * 0.045)
            font = ImageFont.truetype("arialbd.ttf", font_size)
        except Exception:
            font = ImageFont.load_default()

        if subtitle_text:
            import textwrap
            wrapped_lines = textwrap.wrap(subtitle_text, width=24 if width < height else 45)
            line_height = int(height * 0.055)
            start_y = int(height * 0.78)

            # Draw subtitle background banner
            banner_height = len(wrapped_lines) * line_height + 30
            overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
            odraw = ImageDraw.Draw(overlay)
            odraw.rectangle([0, start_y - 15, width, start_y + banner_height], fill=(0, 0, 0, 160))
            img = Image.alpha_composite(img, overlay)
            draw = ImageDraw.Draw(img)

            for i, line in enumerate(wrapped_lines):
                ly = start_y + (i * line_height)
                bbox = draw.textbbox((0, 0), line, font=font)
                text_w = bbox[2] - bbox[0]
                lx = (width - text_w) // 2

                # Text outline
                stroke = 4
                for dx in range(-stroke, stroke + 1):
                    for dy in range(-stroke, stroke + 1):
                        draw.text((lx + dx, ly + dy), line, font=font, fill=(0, 0, 0, 255))
                # Text fill
                draw.text((lx, ly), line, font=font, fill=(255, 235, 59, 255))

        img.convert("RGB").save(dest_path, quality=95)

    def _get_audio_duration(self, audio_path: Path) -> float:
        cmd = [
            "ffprobe", "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            str(audio_path)
        ]
        try:
            res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
            return float(res.stdout.strip())
        except Exception:
            return 15.0

if __name__ == "__main__":
    renderer = VideoRenderer()
    print("VideoRenderer module ready.")
