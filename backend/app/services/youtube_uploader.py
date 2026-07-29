import os
import json
from pathlib import Path
from typing import Dict, Any
from app.config import CLIENT_SECRETS_FILE, OAUTH_TOKENS_DIR

class YouTubeUploader:
    def __init__(self):
        pass

    def upload_video(self, 
                     channel_id: str, 
                     video_path: Path, 
                     title: str, 
                     description: str, 
                     tags: list, 
                     thumbnail_path: Path = None,
                     category_id: str = "27", # 27 = Education, 1 = Film & Animation
                     is_kids: bool = True,
                     privacy_status: str = "public") -> Dict[str, Any]:
        """
        Uploads video to YouTube via Data API v3 using permanent refresh token credentials.
        Auto-refreshes expired access tokens seamlessly.
        """
        token_file = OAUTH_TOKENS_DIR / f"{channel_id}_token.json"
        
        if token_file.exists():
            try:
                from google.oauth2.credentials import Credentials
                from google.auth.transport.requests import Request
                from googleapiclient.discovery import build
                from googleapiclient.http import MediaFileUpload

                with open(token_file, "r", encoding="utf-8") as f:
                    token_info = json.load(f)

                creds = Credentials.from_authorized_user_info(token_info)

                # Auto-refresh expired access tokens in background
                if creds.expired and creds.refresh_token:
                    print(f"Refreshing YouTube OAuth token for channel {channel_id}...")
                    creds.refresh(Request())
                    # Save refreshed token
                    with open(token_file, "w", encoding="utf-8") as f:
                        f.write(creds.to_json())

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
            return {
                "status": "queued_local",
                "message": "Video rendered and saved locally. Connect YouTube OAuth in Channel Manager to auto-post.",
                "video_path": str(video_path)
            }

if __name__ == "__main__":
    uploader = YouTubeUploader()
    print("YouTubeUploader module ready with permanent refresh token auto-renewal.")
