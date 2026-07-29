import scrapetube
from youtube_transcript_api import YouTubeTranscriptApi
from typing import List, Dict, Any

class TrendScraper:
    def __init__(self):
        pass

    def search_trending_topics(self, query: str = "çocuk masalları", max_results: int = 8) -> List[Dict[str, Any]]:
        """
        Searches YouTube for trending videos on a query, returning titles, video IDs, and view indicators.
        """
        results = []
        try:
            videos = scrapetube.get_search(query, limit=max_results)
            for video in videos:
                vid_id = video.get("videoId")
                title = video.get("title", {}).get("runs", [{}])[0].get("text", "Trending Video")
                view_text = video.get("viewCountText", {}).get("simpleText", "N/A views")
                published = video.get("publishedTimeText", {}).get("simpleText", "Recently")
                thumbnail = f"https://i.ytimg.com/vi/{vid_id}/hqdefault.jpg"

                results.append({
                    "id": vid_id,
                    "title": title,
                    "views": view_text,
                    "published": published,
                    "thumbnail": thumbnail,
                    "url": f"https://www.youtube.com/watch?v={vid_id}"
                })
        except Exception as e:
            print(f"Error scraping trends: {e}")
            # Fallback mock trend topics for children's channels
            results = [
                {
                    "id": "mock_1",
                    "title": "Pamuk Kuyruklu Tavşan ve Sihirli Bahçe | Çizgi Film Masal",
                    "views": "1.2M views",
                    "published": "2 days ago",
                    "thumbnail": "https://images.unsplash.com/photo-1579783902614-a3fb3927b675?w=500",
                    "url": "https://www.youtube.com/watch?v=mock_1"
                },
                {
                    "id": "mock_2",
                    "title": "Küçük Ejderha Kuki ve Ateş Çiçeği | Eğitici Masallar",
                    "views": "850K views",
                    "published": "4 days ago",
                    "thumbnail": "https://images.unsplash.com/photo-1563089145-599997674d42?w=500",
                    "url": "https://www.youtube.com/watch?v=mock_2"
                },
                {
                    "id": "mock_3",
                    "title": "Uzay Yolcusu Leo ve Kayıp Yıldız | Çocuk Hikayesi",
                    "views": "2.4M views",
                    "published": "1 week ago",
                    "thumbnail": "https://images.unsplash.com/photo-1534447677768-be436bb09401?w=500",
                    "url": "https://www.youtube.com/watch?v=mock_3"
                }
            ]
        return results

    def get_transcript(self, video_id: str) -> str:
        """Extracts transcript text from a YouTube video if available."""
        try:
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['tr', 'en'])
            full_text = " ".join([item['text'] for item in transcript_list])
            return full_text
        except Exception as e:
            print(f"Could not retrieve transcript for {video_id}: {e}")
            return "Transcript not available."

if __name__ == "__main__":
    ts = TrendScraper()
    print("Scraping Kids Trends...")
    res = ts.search_trending_topics("çocuk çizgi film masalları", max_results=3)
    print("Found Trends:", res)
