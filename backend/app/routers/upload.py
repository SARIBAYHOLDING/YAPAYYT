import os
import json
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from pathlib import Path
from app.config import CLIENT_SECRETS_FILE, OAUTH_TOKENS_DIR
from app.db import get_db

router = APIRouter(prefix="/api/upload", tags=["upload"])

@router.get("/auth-url/{channel_id}")
def get_auth_url(channel_id: str):
    if not CLIENT_SECRETS_FILE.exists():
        # Auto-create template client_secrets.json for user convenience
        default_secrets = {
            "installed": {
                "client_id": "YOUR_CLIENT_ID.apps.googleusercontent.com",
                "project_id": "saribay-youtube-auto",
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                "client_secret": "YOUR_CLIENT_SECRET",
                "redirect_uris": ["http://localhost:8000/api/upload/oauth2callback"]
            }
        }
        with open(CLIENT_SECRETS_FILE, "w", encoding="utf-8") as f:
            json.dump(default_secrets, f, indent=2)

        return {
            "status": "template_created",
            "message": "storage/client_secrets.json şablonu oluşturuldu. Lütfen Google Cloud Client ID ve Secret değerlerinizi buraya yapıştırın.",
            "auth_url": None
        }

    try:
        from google_auth_oauthlib.flow import Flow
        flow = Flow.from_client_secrets_file(
            str(CLIENT_SECRETS_FILE),
            scopes=[
                "https://www.googleapis.com/auth/youtube.upload",
                "https://www.googleapis.com/auth/youtube.readonly"
            ],
            redirect_uri="http://localhost:8000/api/upload/oauth2callback"
        )
        auth_url, _ = flow.authorization_url(
            access_type="offline",
            include_granted_scopes="true",
            prompt="consent",
            state=channel_id
        )
        return {"status": "success", "auth_url": auth_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/oauth2callback")
def oauth2callback(request: Request, code: str = None, state: str = None):
    channel_id = state
    if not code or not channel_id:
        return HTMLResponse("<h2>Hata: OAuth Yetkilendirme kodu bulunamadı.</h2>", status_code=400)

    try:
        from google_auth_oauthlib.flow import Flow
        flow = Flow.from_client_secrets_file(
            str(CLIENT_SECRETS_FILE),
            scopes=[
                "https://www.googleapis.com/auth/youtube.upload",
                "https://www.googleapis.com/auth/youtube.readonly"
            ],
            redirect_uri="http://localhost:8000/api/upload/oauth2callback"
        )
        flow.fetch_token(code=code)
        credentials = flow.credentials

        token_data = {
            "token": credentials.token,
            "refresh_token": credentials.refresh_token,
            "token_uri": credentials.token_uri,
            "client_id": credentials.client_id,
            "client_secret": credentials.client_secret,
            "scopes": credentials.scopes
        }

        token_file = OAUTH_TOKENS_DIR / f"{channel_id}_token.json"
        with open(token_file, "w", encoding="utf-8") as f:
            json.dump(token_data, f, indent=2)

        # Update DB channel status
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("UPDATE channels SET oauth_connected = 1 WHERE id = ?", (channel_id,))
        conn.commit()
        conn.close()

        return HTMLResponse(f"""
        <html>
            <body style="font-family: Arial; text-align: center; padding: 50px; background: #07090E; color: #FFF;">
                <h1 style="color: #34D399;">✅ YouTube Kanal Yetkilendirmesi Başarılı!</h1>
                <p>Kanal ID: <strong>{channel_id}</strong> kalıcı olarak bağlandı.</p>
                <p>Artık tüm videolarınız tam otomatik olarak bu kanala yayınlanacaktır.</p>
                <br/>
                <a href="http://localhost:5173/" style="background: #6366F1; color: #FFF; padding: 12px 24px; border-radius: 8px; text-decoration: none; font-weight: bold;">Sarıbay Studio'ya Dön</a>
            </body>
        </html>
        """)
    except Exception as e:
        return HTMLResponse(f"<h2>OAuth Bağlantı Hatası: {e}</h2>", status_code=500)
