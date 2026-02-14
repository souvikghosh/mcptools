"""Stock market data tools using yfinance."""

from datetime import datetime, timedelta

import yfinance as yf


def get_stock_quote(ticker: str) -> dict:
    """Get the current stock quote for a ticker symbol.

    Returns price, change, volume, market cap, and other key metrics.
    """
    stock = yf.Ticker(ticker)
    info = stock.info

    return {
        "ticker": ticker.upper(),
        "name": info.get("shortName", "N/A"),
        "price": info.get("currentPrice") or info.get("regularMarketPrice"),
        "previous_close": info.get("previousClose"),
        "open": info.get("open") or info.get("regularMarketOpen"),
        "day_high": info.get("dayHigh") or info.get("regularMarketDayHigh"),
        "day_low": info.get("dayLow") or info.get("regularMarketDayLow"),
        "volume": info.get("volume") or info.get("regularMarketVolume"),
        "market_cap": info.get("marketCap"),
        "pe_ratio": info.get("trailingPE"),
        "52_week_high": info.get("fiftyTwoWeekHigh"),
        "52_week_low": info.get("fiftyTwoWeekLow"),
        "currency": info.get("currency", "USD"),
    }


def get_price_history(ticker: str, period: str = "1mo", interval: str = "1d") -> dict:
    """Get historical price data for a ticker.

    Args:
        ticker: Stock ticker symbol
        period: Time period — 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, max
        interval: Data interval — 1m, 5m, 15m, 1h, 1d, 1wk, 1mo
    """
    stock = yf.Ticker(ticker)
    hist = stock.history(period=period, interval=interval)

    if hist.empty:
        return {"ticker": ticker.upper(), "period": period, "data": []}

    records = []
    for date, row in hist.iterrows():
        records.append({
            "date": date.strftime("%Y-%m-%d"),
            "open": round(row["Open"], 2),
            "high": round(row["High"], 2),
            "low": round(row["Low"], 2),
            "close": round(row["Close"], 2),
            "volume": int(row["Volume"]),
        })

    return {
        "ticker": ticker.upper(),
        "period": period,
        "interval": interval,
        "data_points": len(records),
        "data": records,
    }


def get_technical_indicators(ticker: str) -> dict:
    """Calculate basic technical indicators for a stock.

    Computes SMA(20), SMA(50), SMA(200), RSI(14), and price vs. moving averages.
    """
    stock = yf.Ticker(ticker)
    hist = stock.history(period="1y", interval="1d")

    if hist.empty or len(hist) < 20:
        return {"ticker": ticker.upper(), "error": "Insufficient data"}

    closes = hist["Close"]

    # Simple Moving Averages
    sma_20 = round(closes.tail(20).mean(), 2)
    sma_50 = round(closes.tail(50).mean(), 2) if len(closes) >= 50 else None
    sma_200 = round(closes.tail(200).mean(), 2) if len(closes) >= 200 else None

    # RSI (Relative Strength Index) — 14-period
    delta = closes.diff()
    gain = delta.where(delta > 0, 0.0).tail(14).mean()
    loss = (-delta.where(delta < 0, 0.0)).tail(14).mean()
    rs = gain / loss if loss != 0 else 100
    rsi = round(100 - (100 / (1 + rs)), 2)

    current_price = round(closes.iloc[-1], 2)

    return {
        "ticker": ticker.upper(),
        "current_price": current_price,
        "sma_20": sma_20,
        "sma_50": sma_50,
        "sma_200": sma_200,
        "rsi_14": rsi,
        "above_sma_20": current_price > sma_20,
        "above_sma_50": current_price > sma_50 if sma_50 else None,
        "above_sma_200": current_price > sma_200 if sma_200 else None,
        "rsi_signal": "overbought" if rsi > 70 else ("oversold" if rsi < 30 else "neutral"),
    }
