"""Financial news aggregation via RSS feeds."""

from datetime import datetime

import feedparser
import httpx

from mcptools.config import settings


def get_financial_news(query: str | None = None, max_results: int = 10) -> dict:
    """Fetch financial news from Yahoo Finance RSS.

    Args:
        query: Optional search query to filter news
        max_results: Maximum number of articles to return
    """
    url = settings.news_rss_url
    if query:
        url = f"{url}?s={query}"

    feed = feedparser.parse(url)

    articles = []
    for entry in feed.entries[:max_results]:
        published = ""
        if hasattr(entry, "published_parsed") and entry.published_parsed:
            published = datetime(*entry.published_parsed[:6]).isoformat()

        articles.append({
            "title": entry.get("title", ""),
            "summary": entry.get("summary", ""),
            "link": entry.get("link", ""),
            "published": published,
            "source": entry.get("source", {}).get("title", "Yahoo Finance"),
        })

    return {
        "query": query,
        "count": len(articles),
        "articles": articles,
    }


async def get_ticker_news(ticker: str, max_results: int = 5) -> dict:
    """Get news articles specifically about a stock ticker.

    Uses Yahoo Finance RSS filtered by ticker symbol.
    """
    url = f"https://feeds.finance.yahoo.com/rss/2.0/headline?s={ticker}&region=US&lang=en-US"

    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(url)
        response.raise_for_status()

    feed = feedparser.parse(response.text)

    articles = []
    for entry in feed.entries[:max_results]:
        published = ""
        if hasattr(entry, "published_parsed") and entry.published_parsed:
            published = datetime(*entry.published_parsed[:6]).isoformat()

        articles.append({
            "title": entry.get("title", ""),
            "summary": entry.get("summary", ""),
            "link": entry.get("link", ""),
            "published": published,
        })

    return {
        "ticker": ticker.upper(),
        "count": len(articles),
        "articles": articles,
    }
