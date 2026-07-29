# 🚀 Sarıbay AI YouTube Automation Studio

**Sarıbay AI YouTube Automation Studio**, Selahattin Sarıbay (**Sarıbay Yazılım**) tarafından geliştirilmiş; birden fazla YouTube kanalını tam otonom yöneten, yapay zeka ile senaryo yazıp Türkçe doğal seslendiren, 1080p çizgi film/görsel çizen ve videoları tamamen **0 TL sıfır maliyetle** otomatik üreten ve paylaşan gelişmiş bir otomasyon sistemidir.

---

## 🌟 Ana Özellikler

- 🤖 **Tam Otonom Kanal Yönetimi**: Günde belirlenen sayıda videoyu arka planda kendisi üretir ve yayınlar.
- 🗣️ **%100 Ücretsiz Doğal Seslendirme (Microsoft Edge Neural TTS)**: `tr-TR-EmelNeural` (Kadın masal sesi) ve `tr-TR-AhmetNeural` (Erkek anlatıcı sesi) ile sınırsız Türkçe seslendirme ve otomatik SRT alt yazı zamanlaması.
- 🎨 **Sıfır Maliyetli AI Görsel Çizim Motoru (Pollinations AI Flux)**: API anahtarı gerektirmeden 1080p canlı masal ve animasyon sahneleri çizer.
- 🖼️ **Yüksek CTR Kapak Görseli (Thumbnail Builder)**: Dikkat çekici tipografi, renkli zıt renkler ve parlak çerçeveli kapak görselleri.
- 🎬 **FFmpeg & MoviePy 1080p Render Motoru**: 9:16 Shorts ve 16:9 Uzun Format video desteği, Ken Burns kamerası ve sarı/siyah konturlu alt yazılar.
- 🕵️ **Trend & Rakip Kanal Araştırması**: YouTube'da en çok izlenen çocuk kanallarını tarayıp içerikleri telifsiz ve özgün hale getirir.
- 📊 **Modern Glassmorphic Dark UI**: Şık ve canlı kontrollü React Web Dashboard.

---

## 📁 Proje Yapısı

```
YPYZKYYT/
├── backend/
│   ├── app/
│   │   ├── main.py                  # FastAPI Ana Uygulaması
│   │   ├── config.py                # Ayarlar ve Varsayılan Yapılandırma
│   │   ├── db.py                    # SQLite Veritabanı
│   │   ├── routers/                 # API Uç Noktaları (Channels, Videos, Trends, Settings)
│   │   └── services/                # Otomasyon Servisleri (TTS, Image, Render, Uploader, Scheduler)
│   └── requirements.txt             # Python Bağımlılıkları
├── frontend/
│   ├── src/
│   │   ├── App.jsx                  # Ana React Uygulaması
│   │   ├── index.css                # Dark Glassmorphism Tasarım Sistemi
│   │   ├── views/                   # Dashboard, Generator, Channels, Trends, Studio, Settings
│   │   └── components/              # Sidebar, Header
│   └── package.json                 # Frontend Bağımlılıkları
├── storage/                         # Üretilen Ses, Görsel, Video ve Kapak Resimleri
├── vercel.json                      # Vercel Dağıtım Yapılandırması
└── README.md
```

---

## ⚡ Hızlı Başlatma Rehberi

### 1. Yerel Ortam Kurulumu

```bash
# Projeyi klonlayın
git clone https://github.com/SARIBAYHOLDING/YAPAYYT.git
cd YAPAYYT

# Python Sanal Ortamını Hazırlayın
python -m venv venv
venv\Scripts\activate

# Bağımlılıkları yükleyin
pip install -r backend/requirements.txt
```

### 2. Backend Sunucusunu Başlatın (Port 8000)

```bash
cd backend
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

### 3. Frontend Web Arayüzünü Başlatın (Port 5173)

```bash
cd frontend
npm install
npm run dev
```

Arayüze erişmek için tarayıcınızda **http://localhost:5173/** adresini açın!

---

## 🌐 Vercel Dağıtımı (Deployment)

Projeyi Vercel üzerinde canlıya almak için:
1. GitHub reponuzu ([SARIBAYHOLDING/YAPAYYT](https://github.com/SARIBAYHOLDING/YAPAYYT.git)) Vercel hesabınıza bağlayın.
2. Root dizinde `vercel.json` otomatik algılanacak ve dashboard canlıya alınacaktır.

---

## 👨‍💻 Geliştirici & Lisans

- **Geliştirici**: Selahattin Sarıbay
- **Firma**: Sarıbay Yazılım
- **Lisans**: MIT License (Tüm Hakları Sarıbay Holding'e Aittir)
