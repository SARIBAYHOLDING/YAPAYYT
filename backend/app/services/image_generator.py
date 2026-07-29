import os
import urllib.parse
import requests
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random
import time

class ImageGenerator:
    def __init__(self):
        pass

    def generate_ai_image(self, prompt: str, output_path: Path, width: int = 1080, height: int = 1920, style_preset: str = "kids_stories") -> str:
        """
        Generates zero-cost AI Image using Pollinations AI (Flux / SDXL model).
        Fallback to canvas generator if API is unreachable.
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Style enhancements
        style_prompts = {
            "kids_stories": "cute 3d pixar animation style, vibrant colors, friendly character, fairytale illustration, highly detailed, master piece",
            "kids_learning": "bright colorful 3d illustration for children, educational, cute playful objects, clean soft studio lighting",
            "bedtime_tales": "dreamy magical fairytale night scene, soft cozy glow, starry sky, peaceful watercolor fantasy art",
            "ai_tech_facts": "futuristic cyber tech neon glowing background, 8k resolution, cinematic lighting, photorealistic hyperdetailed",
            "facts_mysteries": "cinematic dark dramatic lighting, high contrast, mysterious atmosphere, atmospheric photorealistic"
        }

        enhanced_prompt = f"{prompt}, {style_prompts.get(style_preset, style_prompts['kids_stories'])}"
        encoded_prompt = urllib.parse.quote(enhanced_prompt)

        seed = random.randint(1000, 999999)
        url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={width}&height={height}&seed={seed}&model=flux&nologo=true"

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }

        try:
            response = requests.get(url, headers=headers, timeout=8)
            if response.status_code == 200 and len(response.content) > 5000:
                with open(output_path, "wb") as f:
                    f.write(response.content)
                return str(output_path)
        except Exception as e:
            print(f"Pollinations AI image generation error/timeout: {e}. Switching to dynamic canvas fallback.")

        # Fallback local canvas generation
        self._generate_fallback_canvas(prompt, output_path, width, height)
        return str(output_path)

    def _generate_fallback_canvas(self, title_text: str, output_path: Path, width: int, height: int):
        """Creates a sleek gradient background image with title overlay as fallback."""
        img = Image.new("RGB", (width, height), color=(20, 24, 40))
        draw = ImageDraw.Draw(img)

        # Create elegant radial gradient
        for y in range(height):
            r = int(25 + (y / height) * 35)
            g = int(30 + (y / height) * 45)
            b = int(70 + (y / height) * 90)
            draw.line([(0, y), (width, y)], fill=(r, g, b))

        # Add decorative glowing shapes
        for _ in range(5):
            cx = random.randint(100, width - 100)
            cy = random.randint(100, height - 100)
            radius = random.randint(150, 400)
            color = random.choice([(255, 105, 180, 50), (0, 206, 209, 50), (255, 215, 0, 50)])
            overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
            odraw = ImageDraw.Draw(overlay)
            odraw.ellipse([cx - radius, cy - radius, cx + radius, cy + radius], fill=color)
            overlay = overlay.filter(ImageFilter.GaussianBlur(80))
            img.paste(overlay, (0, 0), overlay)

        img.save(output_path, quality=95)

if __name__ == "__main__":
    gen = ImageGenerator()
    out = gen.generate_ai_image("A cute little fox exploring an enchanted glowing forest at night", Path("../../storage/test_ai_image.jpg"), 1080, 1920, "kids_stories")
    print("AI Image Generated:", out)
