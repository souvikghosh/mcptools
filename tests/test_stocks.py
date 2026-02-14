"""Tests for stock data tools (mocked — no real API calls)."""

from unittest.mock import MagicMock, patch
import pytest
import pandas as pd
import numpy as np

from mcptools.tools.stocks import get_stock_quote, get_price_history, get_technical_indicators


@pytest.fixture
def mock_ticker_info():
    return {
        "shortName": "Apple Inc.",
        "currentPrice": 195.50,
        "previousClose": 194.00,
        "open": 194.50,
        "dayHigh": 196.00,
        "dayLow": 193.50,
        "volume": 45_000_000,
        "marketCap": 3_000_000_000_000,
        "trailingPE": 30.5,
        "fiftyTwoWeekHigh": 199.62,
        "fiftyTwoWeekLow": 164.08,
        "currency": "USD",
    }


class TestGetStockQuote:
    @patch("mcptools.tools.stocks.yf.Ticker")
    def test_returns_quote_data(self, mock_yf, mock_ticker_info):
        mock_yf.return_value.info = mock_ticker_info
        result = get_stock_quote("AAPL")

        assert result["ticker"] == "AAPL"
        assert result["name"] == "Apple Inc."
        assert result["price"] == 195.50
        assert result["market_cap"] == 3_000_000_000_000
        assert result["pe_ratio"] == 30.5

    @patch("mcptools.tools.stocks.yf.Ticker")
    def test_ticker_uppercased(self, mock_yf, mock_ticker_info):
        mock_yf.return_value.info = mock_ticker_info
        result = get_stock_quote("aapl")
        assert result["ticker"] == "AAPL"


class TestGetPriceHistory:
    @patch("mcptools.tools.stocks.yf.Ticker")
    def test_returns_history(self, mock_yf):
        dates = pd.date_range("2024-01-01", periods=5, freq="D")
        hist = pd.DataFrame({
            "Open": [190.0, 191.0, 192.0, 193.0, 194.0],
            "High": [191.0, 192.0, 193.0, 194.0, 195.0],
            "Low": [189.0, 190.0, 191.0, 192.0, 193.0],
            "Close": [190.5, 191.5, 192.5, 193.5, 194.5],
            "Volume": [1000000] * 5,
        }, index=dates)
        mock_yf.return_value.history.return_value = hist

        result = get_price_history("AAPL", period="5d")
        assert result["ticker"] == "AAPL"
        assert result["data_points"] == 5
        assert len(result["data"]) == 5
        assert "close" in result["data"][0]

    @patch("mcptools.tools.stocks.yf.Ticker")
    def test_empty_history(self, mock_yf):
        mock_yf.return_value.history.return_value = pd.DataFrame()
        result = get_price_history("INVALID")
        assert result["data"] == []


class TestGetTechnicalIndicators:
    @patch("mcptools.tools.stocks.yf.Ticker")
    def test_returns_indicators(self, mock_yf):
        dates = pd.date_range("2024-01-01", periods=250, freq="D")
        np.random.seed(42)
        prices = 100 + np.cumsum(np.random.randn(250) * 0.5)
        hist = pd.DataFrame({
            "Open": prices,
            "High": prices + 1,
            "Low": prices - 1,
            "Close": prices,
            "Volume": [1000000] * 250,
        }, index=dates)
        mock_yf.return_value.history.return_value = hist

        result = get_technical_indicators("AAPL")
        assert result["ticker"] == "AAPL"
        assert "sma_20" in result
        assert "sma_50" in result
        assert "sma_200" in result
        assert "rsi_14" in result
        assert result["rsi_signal"] in ("overbought", "oversold", "neutral")

    @patch("mcptools.tools.stocks.yf.Ticker")
    def test_insufficient_data(self, mock_yf):
        dates = pd.date_range("2024-01-01", periods=5, freq="D")
        hist = pd.DataFrame({
            "Close": [100, 101, 102, 103, 104],
        }, index=dates)
        mock_yf.return_value.history.return_value = hist
        result = get_technical_indicators("NEW")
        assert "error" in result
