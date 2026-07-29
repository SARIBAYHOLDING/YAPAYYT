import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(r"c:\Users\ssari\Desktop\YPYZKYYT\backend")))

from app.services.scheduler_service import SchedulerService

def run():
    print("==================================================================")
    print("4 ULTRA HD YOUTUBE VIDEOSU 2 FARKLI KANALDA URETILIYOR...")
    print("==================================================================")

    svc = SchedulerService()

    # 1. Channel 1 - Video 1
    print("\n[1/4] Kanal: ch_kids_main (Sevimli Masal Dunyasi)")
    v1 = svc.generate_and_publish_for_channel("ch_kids_main", "Sihirli Ormanin Kayip Yildizi Ve Sevimli Tavsan Pamuk")
    print(f"Video 1 Uretildi & Siraya Alindi! ID: {v1}")

    # 2. Channel 1 - Video 2
    print("\n[2/4] Kanal: ch_kids_main (Sevimli Masal Dunyasi)")
    v2 = svc.generate_and_publish_for_channel("ch_kids_main", "Rengarenk Balik Boncugun Okyanus Gezisi Ve Sevimli Yunus")
    print(f"Video 2 Uretildi & Siraya Alindi! ID: {v2}")

    # 3. Channel 2 - Video 3
    print("\n[3/4] Kanal: ch_tech_main (AI Teknoloji Rehberi)")
    v3 = svc.generate_and_publish_for_channel("ch_tech_main", "2030 Yilinda Yasamimizi Degistirecek 5 Inanilmaz Yapay Zeka Devrimi")
    print(f"Video 3 Uretildi & Siraya Alindi! ID: {v3}")

    # 4. Channel 2 - Video 4
    print("\n[4/4] Kanal: ch_tech_main (AI Teknoloji Rehberi)")
    v4 = svc.generate_and_publish_for_channel("ch_tech_main", "Kuantum Bilgisayarlar Ve Gelecegin Otonom Smart Akilli Sehirleri")
    print(f"Video 4 Uretildi & Siraya Alindi! ID: {v4}")

    print("\n==================================================================")
    print("TEBRILER! 2 KANALDA TOPLAM 4 ADET ULTRA HD VIDEO YAYINLANDI!")
    print("==================================================================")

if __name__ == "__main__":
    run()
