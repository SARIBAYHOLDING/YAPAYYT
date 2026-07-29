import os
import json
import re
from typing import Dict, Any, List
from app.config import GEMINI_API_KEY, NICHES

class ScriptGenerator:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or GEMINI_API_KEY or os.environ.get("GEMINI_API_KEY", "")

    def generate_script(self, topic: str, niche: str = "kids_stories", format_type: str = "shorts", language: str = "tr") -> Dict[str, Any]:
        """
        Generates a complete YouTube script, scene breakdown, title, description, and tags.
        Uses Gemini API if available, or structured fallback generator.
        """
        niche_info = NICHES.get(niche, NICHES["kids_stories"])
        target_scene_count = 5 if format_type == "shorts" else 12

        if self.api_key:
            try:
                return self._call_gemini(topic, niche_info, format_type, language, target_scene_count)
            except Exception as e:
                print(f"Gemini API call warning: {e}. Using intelligent template generator.")

        return self._generate_template_script(topic, niche, format_type, language, target_scene_count)

    def _call_gemini(self, topic: str, niche_info: Dict[str, Any], format_type: str, language: str, scene_count: int) -> Dict[str, Any]:
        from google import genai
        from google.genai import types

        client = genai.Client(api_key=self.api_key)
        
        prompt = f"""
        Sen YouTube viral içerik uzmanı ve çocuk masalları / ilgi çekici video senaristisin.
        Konu: "{topic}"
        Niş: {niche_info['name']} ({niche_info['description']})
        Video Formatı: {format_type.upper()} (9:16 Shorts veya 16:9 Uzun Video)
        Dil: {language.upper()}

        Lütfen tam olarak aşağıdaki JSON formatında yanıt ver. Başka hiçbir açıklama yazma, sadece saf JSON dök.
        {{
            "title": "Çok merak uyandırıcı, büyük harflerle dikkat çeken YouTube başlığı",
            "description": "SEO uyumlu, anahtar kelimeli ve etkileşim çağıran açıklama metni",
            "tags": ["etiket1", "etiket2", "etiket3", "etiket4", "etiket5"],
            "scenes": [
                {{
                    "scene_num": 1,
                    "narration": "Seslendirilecek Türkçe veya ilgili dildeki konuşma metni. Merak uyandırıcı ve akıcı olmalı.",
                    "visual_prompt": "English detailed visual prompt for AI image generator depicting this scene clearly."
                }}
            ]
        }}
        {scene_count} adet sahne oluştur.
        """

        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            )
        )

        data = json.loads(response.text)
        return data

    def _generate_template_script(self, topic: str, niche: str, format_type: str, language: str, scene_count: int) -> Dict[str, Any]:
        """High quality zero-cost template script generator."""
        clean_topic = topic.strip()
        
        if niche == "kids_stories":
            title = f"🐾 {clean_topic.upper()} | SEVİMLİ ORMAN MACERASI"
            desc = f"Harika bir çocuk masalı! {clean_topic} ile macera dolu eğlenceli bir yolculuğa hazır mısınız? Kanalımıza abone olmayı ve beğenmeyi unutmayın! ✨"
            tags = ["çocuk masalları", "çocuk hikayeleri", "animasyon masal", "eğitici masallar", "bebek masalları"]
            scenes = [
                {
                    "scene_num": 1,
                    "narration": f"Bir zamanlar, rüya gibi renkli ve büyülü bir ormanda {clean_topic} adında sevimli bir dostumuz yaşarmış.",
                    "visual_prompt": f"Cute friendly animal character named {clean_topic} in a colorful fairytale magical forest, 3d pixar style, warm lighting"
                },
                {
                    "scene_num": 2,
                    "narration": "Bir sabah uyandığında ormanın en derin köşesinden gelen gizemli ve pırıl pırıl bir ışık fark etmiş.",
                    "visual_prompt": "Magical glowing light deep in a fairytale forest with cute little animals looking curious, 3d vibrant animation"
                },
                {
                    "scene_num": 3,
                    "narration": "Cesaretini toplayıp arkadaşlarıyla birlikte bu harika ışığın peşinden gitmeye karar vermiş.",
                    "visual_prompt": "Group of cute small woodland animals walking together happily on a cobblestone path, 3d disney style"
                },
                {
                    "scene_num": 4,
                    "narration": "Yolun sonunda lezzetli meyveler ve rengarenk kelebeklerle dolu gizli bir bahçe bulmuşlar!",
                    "visual_prompt": "Secret fairy garden filled with giant glowing fruits and colorful butterflies, magical lighting, cute 3d rendering"
                },
                {
                    "scene_num": 5,
                    "narration": "Birlikte paylaşmanın ve dostluğun ne kadar değerli olduğunu bir kez daha anlamışlar. Daha fazla masal için abone olun!",
                    "visual_prompt": "Cute animals celebrating happily around a tree, friendly smiling faces, cozy fairytale ending, 3d render"
                }
            ]
        elif niche == "ai_tech_facts":
            title = f"⚡ {clean_topic.upper()} | DUYDUĞUNUZDA İNANAMAYACAKSINIZ!"
            desc = f"Geleceğin teknolojisi ve yapay zeka hakkında 5 şaşırtıcı bilgi! {clean_topic} detayları videoda. Abone ol: @SarıbayStudio"
            tags = ["yapay zeka", "teknoloji", "ilginç bilgiler", "gelecek", "bilim"]
            scenes = [
                {
                    "scene_num": 1,
                    "narration": f"Gelecek düşündüğünüzden çok daha hızlı geliyor! {clean_topic} hakkında bilmeniz gereken harika gerçekler.",
                    "visual_prompt": f"Futuristic high tech holographic visualization of {clean_topic}, neon blue and purple background, 8k resolution"
                },
                {
                    "scene_num": 2,
                    "narration": "Yapay zeka sistemleri artık insan beyninden 1000 kat daha hızlı veri işleme kapasitesine ulaştı.",
                    "visual_prompt": "Futuristic glowing AI digital brain with glowing fiber optic neural network nodes, cyber aesthetic"
                },
                {
                    "scene_num": 3,
                    "narration": "Yakın gelecekte günlük işlerimizin %80'ini otonom akıllı ajanlar gerçekleştirecek.",
                    "visual_prompt": "Advanced humanoid robot assisting in a high tech smart city control room, cinematic lighting"
                },
                {
                    "scene_num": 4,
                    "narration": "Bu dönüşüme hazır mısınız? Teknoloji dünyasındaki gelişmeleri kaçırmamak için Sarıbay Studio'ya abone olmayı unutmayın!",
                    "visual_prompt": "Cyberpunk smart city skyline at night with glowing digital neon pathways and flying vehicles, photorealistic"
                }
            ]
        else:
            title = f"✨ {clean_topic.upper()} | GİZEMLİ GERÇEKLER"
            desc = f"Bilmeyeler için {clean_topic} hakkında en şaşırtıcı detaylar."
            tags = ["bilgi", "trend", "shorts", "youtube"]
            scenes = [
                {
                    "scene_num": 1,
                    "narration": f"Hazır olun! Bugün sizlerle {clean_topic} konusunu inceliyoruz.",
                    "visual_prompt": f"Cinematic atmospheric scene representing {clean_topic}, high quality digital art"
                },
                {
                    "scene_num": 2,
                    "narration": "Bu konuda yapılan araştırmalar herkesi oldukça şaşırtıyor.",
                    "visual_prompt": "Mysterious library with glowing ancient books and magical floating particles"
                },
                {
                    "scene_num": 3,
                    "narration": "Daha fazla heyecan verici içerik için takipte kalın!",
                    "visual_prompt": "Epic sunrise over a magnificent castle, cinematic lighting"
                }
            ]

        return {
            "title": title,
            "description": desc,
            "tags": tags,
            "scenes": scenes
        }

if __name__ == "__main__":
    sg = ScriptGenerator()
    res = sg.generate_script("Pamuk Kuyruk Ve Sihirli Havuç", niche="kids_stories", format_type="shorts")
    print("Generated Script:", json.dumps(res, ensure_ascii=False, indent=2))
