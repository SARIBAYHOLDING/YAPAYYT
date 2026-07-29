from fastapi import APIRouter
from app.services.trend_scraper import TrendScraper

router = APIRouter(prefix="/api/trends", tags=["trends"])
scraper = TrendScraper()

@router.get("/search")
def search_trends(query: str = "çocuk masalları", max_results: int = 8):
    results = scraper.search_trending_topics(query=query, max_results=max_results)
    return {"query": query, "results": results}

@router.get("/transcript")
def get_transcript(video_id: str):
    transcript = scraper.get_transcript(video_id)
    return {"video_id": video_id, "transcript": transcript}
