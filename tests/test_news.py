"""Tests for news aggregation tools (mocked — no real API calls)."""

from unittest.mock import patch, MagicMock
import pytest

from mcptools.tools.news import get_financial_news


class TestGetFinancialNews:
    @patch("mcptools.tools.news.feedparser.parse")
    def test_returns_articles(self, mock_parse):
        # Use SimpleNamespace-like dicts that support .get() via feedparser entries
        entry1 = MagicMock()
        entry1.get = lambda key, default="": {"title": "Market rallies on earnings", "summary": "Stocks rose today as...", "link": "https://example.com/article1", "source": {"title": "Yahoo Finance"}}.get(key, default)
        entry1.published_parsed = (2024, 6, 15, 10, 30, 0, 5, 167, 0)

        entry2 = MagicMock()
        entry2.get = lambda key, default="": {"title": "Fed holds rates steady", "summary": "The Federal Reserve...", "link": "https://example.com/article2", "source": {"title": "Reuters"}}.get(key, default)
        entry2.published_parsed = (2024, 6, 15, 9, 0, 0, 5, 167, 0)

        mock_parse.return_value.entries = [entry1, entry2]

        result = get_financial_news()
        assert result["count"] == 2
        assert result["articles"][0]["title"] == "Market rallies on earnings"
        assert result["articles"][1]["title"] == "Fed holds rates steady"

    @patch("mcptools.tools.news.feedparser.parse")
    def test_respects_max_results(self, mock_parse):
        mock_parse.return_value.entries = [
            MagicMock(
                title=f"Article {i}",
                summary=f"Summary {i}",
                link=f"https://example.com/{i}",
                published_parsed=None,
                source={},
            )
            for i in range(20)
        ]

        result = get_financial_news(max_results=5)
        assert result["count"] == 5

    @patch("mcptools.tools.news.feedparser.parse")
    def test_empty_feed(self, mock_parse):
        mock_parse.return_value.entries = []
        result = get_financial_news()
        assert result["count"] == 0
        assert result["articles"] == []

    @patch("mcptools.tools.news.feedparser.parse")
    def test_query_passed_through(self, mock_parse):
        mock_parse.return_value.entries = []
        result = get_financial_news(query="AAPL")
        assert result["query"] == "AAPL"
