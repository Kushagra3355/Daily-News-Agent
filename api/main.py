from fastapi import FastAPI, HTTPException
from utils.scheduler import run_daily_job
from tools.category_filter import filter_news_by_category
from tools.category_extractor import get_all_categories
import json
import os

app = FastAPI(title="Daily News Summarizer API")


def load_cached_news():
    """Load news summary from cached file."""
    cache_file = "data/news_summary.json"
    if not os.path.exists(cache_file):
        raise HTTPException(
            status_code=404,
            detail="No news data available. Please call /news/refresh first.",
        )

    with open(cache_file, "r") as f:
        return json.load(f)


@app.get("/news/all")
def get_all_news():
    """Get all news summaries from cache."""
    return load_cached_news()


@app.get("/news/category/{category}")
def get_news_by_category(category: str):
    """Get news filtered by category from cache."""
    data = load_cached_news()
    return filter_news_by_category(data, category.lower())


@app.get("/news/categories")
def list_all_categories():
    """Get all available categories from cache."""
    data = load_cached_news()
    return get_all_categories(data)


@app.post("/news/refresh")
def refresh_news():
    """Manually trigger news fetching and summarization."""
    result = run_daily_job()
    return {"message": "News refreshed successfully", "data": result}
