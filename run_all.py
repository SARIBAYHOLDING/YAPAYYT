import subprocess
import time
import webbrowser
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
PYTHON_EXE = BASE_DIR / "venv" / "Scripts" / "python.exe"

def main():
    print("=" * 70)
    print(" 🚀 SARIBAY AI YOUTUBE AUTOMATION STUDIO - MASTER LAUNCHER")
    print(" Geliştirici: Selahattin Sarıbay (Sarıbay Yazılım)")
    print("=" * 70)

    # 1. Start Backend API Server
    print("\n[1/2] Backend Sunucusu Başlatılıyor (Port 8000)...")
    backend_cwd = BASE_DIR / "backend"
    backend_cmd = [str(PYTHON_EXE), "-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8000"]
    backend_proc = subprocess.Popen(backend_cmd, cwd=backend_cwd)

    time.sleep(3)

    # 2. Start Frontend Web Studio
    print("[2/2] Frontend Web Stüdyosu Başlatılıyor (Port 5173)...")
    frontend_cwd = BASE_DIR / "frontend"
    frontend_cmd = ["npm.cmd", "run", "dev"]
    frontend_proc = subprocess.Popen(frontend_cmd, cwd=frontend_cwd, shell=True)

    time.sleep(3)

    print("\n" + "=" * 70)
    print(" ✅ TÜM SUNUCULAR BAŞARIYLA AKTİF EDİLDİ!")
    print(" 🎨 Web Dashboard: http://localhost:5173/")
    print(" ⚙️ Backend API:    http://127.0.0.1:8000")
    print("=" * 70 + "\n")

    # Open Browser
    webbrowser.open("http://localhost:5173/")

    try:
        backend_proc.wait()
        frontend_proc.wait()
    except KeyboardInterrupt:
        print("\nSunucular durduruluyor...")
        backend_proc.terminate()
        frontend_proc.terminate()

if __name__ == "__main__":
    main()
