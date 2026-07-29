import asyncio
import edge_tts
from pathlib import Path
from typing import Dict, Any, List

# Popular Edge TTS voices
AVAILABLE_VOICES = {
    "tr-TR-EmelNeural": "Türkçe - Emel (Kadın, Masal/Hikaye)",
    "tr-TR-AhmetNeural": "Türkçe - Ahmet (Erkek, Enerjik/Teknoloji)",
    "en-US-AnaNeural": "English - Ana (Cute Kids)",
    "en-US-ChristopherNeural": "English - Christopher (Deep Male)",
    "en-US-JennyNeural": "English - Jenny (Storyteller)",
    "de-DE-KatjaNeural": "German - Katja (Female)",
    "es-ES-ElviraNeural": "Spanish - Elvira (Female)"
}

class TTSEngine:
    def __init__(self, voice: str = "tr-TR-EmelNeural", rate: str = "+0%", pitch: str = "+0Hz"):
        self.voice = voice
        self.rate = rate
        self.pitch = pitch

    async def generate_audio_file(self, text: str, output_mp3_path: Path, output_srt_path: Path = None) -> Dict[str, Any]:
        """
        Generates audio file from text using edge-tts and optionally outputs an SRT subtitle file.
        Returns duration and timing markers.
        """
        output_mp3_path = Path(output_mp3_path)
        output_mp3_path.parent.mkdir(parents=True, exist_ok=True)
        
        communicate = edge_tts.Communicate(text, self.voice, rate=self.rate, pitch=self.pitch)
        
        submaker = edge_tts.SubMaker()
        with open(output_mp3_path, "wb") as file:
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    file.write(chunk["data"])
                elif chunk["type"] == "WordBoundary":
                    submaker.create_sub((chunk["offset"], chunk["duration"]), chunk["text"])

        try:
            srt_content = submaker.get_srt()
        except Exception:
            srt_content = submaker.generate_subs() if hasattr(submaker, 'generate_subs') else ""
            
        if output_srt_path:
            output_srt_path = Path(output_srt_path)
            output_srt_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_srt_path, "w", encoding="utf-8") as f:
                f.write(srt_content)
                
        return {
            "audio_path": str(output_mp3_path),
            "srt_path": str(output_srt_path) if output_srt_path else None,
            "voice": self.voice,
            "status": "success"
        }

def generate_tts_sync(text: str, output_mp3_path: str, voice: str = "tr-TR-EmelNeural", output_srt_path: str = None) -> Dict[str, Any]:
    engine = TTSEngine(voice=voice)
    return asyncio.run(engine.generate_audio_file(text, Path(output_mp3_path), Path(output_srt_path) if output_srt_path else None))

if __name__ == "__main__":
    test_text = "Merhaba! Selahattin Sarıbay tarafından geliştirilen sıfır maliyetli yapay zeka YouTube otomasyon sistemine hoş geldiniz."
    res = generate_tts_sync(test_text, "../../storage/test_speech.mp3", voice="tr-TR-EmelNeural", output_srt_path="../../storage/test_speech.srt")
    print("TTS Test Result:", res)
