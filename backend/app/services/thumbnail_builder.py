import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import textwrap
import random

class ThumbnailBuilder:
    def __init__(self):
        pass

    def create_thumbnail(self, background_image_path: Path, title_text: str, output_path: Path, is_shorts: bool = False) -> str:
        """
        Creates a high CTR thumbnail with bold typography, dynamic background contrast, and glowing elements.
        """
        background_image_path = Path(background_image_path)
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        target_width = 1080 if is_shorts else 1280
        target_height = 1920 if is_shorts else 720

        if background_image_path.exists():
            base = Image.open(background_image_path).convert("RGBA")
            base = base.resize((target_width, target_height), Image.Resampling.LANCZOS)
        else:
            base = Image.new("RGBA", (target_width, target_height), (15, 20, 35, 255))

        # Enhance contrast & color saturation
        enhancer = ImageEnhance.Color(base)
        base = enhancer.enhance(1.3)
        enhancer_contrast = ImageEnhance.Contrast(base)
        base = enhancer_contrast.enhance(1.15)

        # Add gradient overlay for dark bottom/top text readability
        overlay = Image.new("RGBA", (target_width, target_height), (0, 0, 0, 0))
        draw_overlay = ImageDraw.Draw(overlay)

        # Dark gradient bar at top/center
        bar_height = int(target_height * 0.45)
        bar_y = int(target_height * (0.55 if is_shorts else 0.5))
        for y in range(bar_height):
            alpha = int(180 * (y / bar_height))
            draw_overlay.line([(0, bar_y + y), (target_width, bar_y + y)], fill=(0, 0, 0, alpha))

        base = Image.alpha_composite(base, overlay)
        draw = ImageDraw.Draw(base)

        # Load font (Fallback to default if custom ttf not present)
        try:
            font_size = int(target_height * 0.075 if is_shorts else target_height * 0.12)
            font = ImageFont.truetype("arial.ttf", font_size)
            badge_font = ImageFont.truetype("arialbd.ttf", int(font_size * 0.6))
        except Exception:
            font = ImageFont.load_default()
            badge_font = ImageFont.load_default()

        # Format title text
        clean_title = title_text.upper()
        lines = textwrap.wrap(clean_title, width=16 if is_shorts else 22)
        if len(lines) > 3:
            lines = lines[:3]

        # Draw Bold Badge ("İZLEMEDEN GEÇME!" / "EĞLENCELİ HİKAYE")
        badge_text = "🔥 YENİ HİKAYE!" if "HİKAYE" in clean_title or is_shorts else "⚡ İNANILMAZ!"
        badge_x, badge_y = 50, bar_y + 20
        draw.rectangle([badge_x, badge_y, badge_x + 320, badge_y + 60], fill=(255, 215, 0, 255))
        draw.text((badge_x + 20, badge_y + 12), badge_text, fill=(0, 0, 0, 255), font=badge_font)

        # Draw Title lines with thick text stroke & shadow
        start_y = bar_y + 90
        for i, line in enumerate(lines):
            line_y = start_y + (i * (font_size + 15))
            
            # Thick black outline
            stroke_width = 8
            for dx in range(-stroke_width, stroke_width + 1):
                for dy in range(-stroke_width, stroke_width + 1):
                    if dx*dx + dy*dy <= stroke_width*stroke_width:
                        draw.text((50 + dx, line_y + dy), line, font=font, fill=(0, 0, 0, 255))

            # Main text color (Yellow & White alternate)
            fill_color = (255, 235, 59, 255) if i % 2 == 0 else (255, 255, 255, 255)
            draw.text((50, line_y), line, font=font, fill=fill_color)

        # Draw glowing outer border
        border_width = 12
        draw.rectangle([0, 0, target_width, target_height], outline=(255, 215, 0, 255), width=border_width)

        base.convert("RGB").save(output_path, quality=95)
        return str(output_path)

if __name__ == "__main__":
    builder = ThumbnailBuilder()
    out = builder.create_thumbnail(
        Path("../../storage/test_ai_image.jpg"),
        "SEVİMLİ ORMAN MACERASI",
        Path("../../storage/test_thumbnail.jpg"),
        is_shorts=True
    )
    print("Thumbnail Generated:", out)
