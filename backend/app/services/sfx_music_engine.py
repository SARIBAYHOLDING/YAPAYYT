import os
import subprocess
import math
from pathlib import Path
from PIL import Image, ImageDraw
import numpy as np
import wave
import struct
from app.config import AUDIO_DIR, TEMP_DIR

class SFXMusicEngine:
    def __init__(self):
        pass

    def create_ambient_music(self, output_wav_path: Path, duration: float, mood: str = "kids_stories") -> str:
        """
        Generates a soothing background ambient music track using synthetic harmonic waves.
        100% royalty free, zero copyright!
        """
        output_wav_path = Path(output_wav_path)
        output_wav_path.parent.mkdir(parents=True, exist_ok=True)

        sample_rate = 44100
        n_samples = int(sample_rate * duration)

        # Base frequencies for different moods
        chords = {
            "kids_stories": [261.63, 329.63, 392.00, 523.25], # C Major pentatonic
            "bedtime_tales": [220.00, 277.18, 329.63, 440.00], # A Minor cozy
            "ai_tech_facts": [146.83, 220.00, 293.66, 440.00], # D Synthwave
            "facts_mysteries": [130.81, 164.81, 196.00, 261.63]
        }
        freqs = chords.get(mood, chords["kids_stories"])

        audio_data = []
        for i in range(n_samples):
            t = i / sample_rate
            # Soft pad wave synthesis
            val = 0
            for idx, f in enumerate(freqs):
                lfo = 0.5 + 0.5 * math.sin(2 * math.pi * 0.2 * t + idx)
                val += math.sin(2 * math.pi * f * t) * 0.15 * lfo

            # Soft fade-in and fade-out
            fade_in = min(1.0, t / 2.0)
            fade_out = min(1.0, (duration - t) / 2.0)
            val *= fade_in * fade_out

            packed_val = int(val * 12000)
            audio_data.append(struct.pack('h', max(-32767, min(32767, packed_val))))

        with wave.open(str(output_wav_path), 'w') as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(sample_rate)
            wav_file.writeframes(b''.join(audio_data))

        return str(output_wav_path)

    def mix_narration_with_music(self, narration_mp3: Path, output_mixed_mp3: Path, mood: str = "kids_stories") -> str:
        """
        Blends narration speech audio with background ambient music using FFmpeg audio filter.
        """
        narration_mp3 = Path(narration_mp3)
        output_mixed_mp3 = Path(output_mixed_mp3)
        output_mixed_mp3.parent.mkdir(parents=True, exist_ok=True)

        # Get narration duration
        cmd_dur = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(narration_mp3)]
        try:
            res = subprocess.run(cmd_dur, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
            duration = float(res.stdout.strip())
        except Exception:
            duration = 15.0

        bg_wav = TEMP_DIR / f"temp_bg_music_{hash(mood)}.wav"
        self.create_ambient_music(bg_wav, duration + 2.0, mood=mood)

        # FFmpeg amix audio filter
        cmd = [
            "ffmpeg", "-y",
            "-i", str(narration_mp3),
            "-i", str(bg_wav),
            "-filter_complex", "[0:a]volume=1.2[a0];[1:a]volume=0.25[a1];[a0][a1]amix=inputs=2:duration=first[aout]",
            "-map", "[aout]",
            "-c:a", "aac",
            "-b:a", "192k",
            str(output_mixed_mp3)
        ]

        try:
            subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
            return str(output_mixed_mp3)
        except Exception as e:
            print(f"Audio mix fallback: {e}. Preserving raw TTS narration file.")
            import shutil
            shutil.copyfile(narration_mp3, output_mixed_mp3)
            return str(output_mixed_mp3)

if __name__ == "__main__":
    sfx = SFXMusicEngine()
    print("SFXMusicEngine module ready.")
