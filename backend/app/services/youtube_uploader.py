import os
import json
from pathlib import Path
from typing import Dict, Any
from app.config import CLIENT_SECRETS_FILE, OAUTH_TOKENS_DIR

class YouTubeUploader:
    def __init__(self):
        pass

    def get_auth_url(self, channel_id: str) -> str:
        """Returns OAuth authorization URL if client_secrets.json is provided."""
        if not CLIENT_SECRETS_FILE.exists():
            return "NO_CLIENT_SECRETS"
        
        try:
            from google_auth_oauthlib.flow import Flow
            flow = Flow.from_client_secrets_file(
                str(CLIENT_SECRETS_FILE),
                scopes=["https://www.googleapis.com/auth/youtube.upload", "https://www.googleapis.com/auth/youtube.readonly"],
                redirect_uri="http://localhost:8000/api/upload/oauth2callback"
            )
            auth_url, _ = flow.authorization_url(prompt="consent", state=channel_id)
            return auth_url
        except Exception as e:
            print(f"Error creating auth URL: {e}")
            return "AUTH_ERROR"

    def upload_video(self, 
                     channel_id: str, 
                     video_path: Path, 
                     title: str, 
                     description: str, 
                     tags: list, 
                     thumbnail_path: Path = None,
                     category_id: str = "27", # 27 = Education, 1 = Film & Animation, 28 = SciTech
                     is_kids: bool = True,
                     privacy_status: str = "public") -> Dict[str, Any]:
        """
        Uploads video to YouTube via Data API v3 if OAuth token exists, or stores in publication queue.
        """
        token_file = OAUTH_TOKENS_DIR / f"{channel_id}_token.json"
        
        if token_file.exists():
            try:
                from google.oauth2.credentials import Credentials
                from googleapiclient.discovery import build
                from googleapiclient.http import MediaFileUpload

                creds = Credentials.from_authorized_user_file(str(token_file))
                youtube = build("youtube", "v3", credentials=creds)

                body = {
                    "snippet": {
                        "title": title[:100],
                        "description": description[:4000],
                        "tags": tags,
                        "categoryId": category_id
                    },
                    "status": {
                        "privacyStatus": privacy_status,
                        "selfDeclaredMadeForKids": is_kids
                    }
                }

                media = MediaFileUpload(str(video_path), chunksize=-1, resumable=True)
                request = youtube.videos().insert(
                    part="snippet,status",
                    body=body,
                    media_body=media
                )
                response = request.execute()
                video_id = response.get("id")

                # Upload thumbnail if present
                if thumbnail_path and os.path.exists(thumbnail_path) and video_id:
                    try:
                        youtube.thumbnails().set(
                            videoId=video_id,
                            media_body=MediaFileUpload(str(thumbnail_path))
                        ).execute()
                    except Exception as e:
                        print(f"Thumbnail upload warning: {e}")

                return {
                    "status": "published",
                    "youtube_video_id": video_id,
                    "youtube_url": f"https://www.youtube.com/watch?v={video_id}"
                }
            except Exception as e:
                print(f"YouTube Upload API error: {e}")
                return {
                    "status": "failed",
                    "error": str(e)
                }
        else:
            # Safe Queue Mode when OAuth is not yet completed
            return {
                "status": "queued_local",
                "message": "Video successfully generated and queued locally. Connect YouTube OAuth to publish automatically.",
                "video_path": str(video_path)
            }

if __name__ == "__main__":
    uploader = YouTubeUploader()
    print("YouTubeUploader module ready.")
