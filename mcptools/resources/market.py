"""Market summary resource endpoints."""

import yfinance as yf


def get_market_summary() -> dict:
    """Get a summary of major market indices and their performance."""
    indices = {
        "^GSPC": "S&P 500",
        "^DJI": "Dow Jones",
        "^IXIC": "NASDAQ",
        "^RUT": "Russell 2000",
        "^VIX": "VIX",
    }

    summary = []
    for symbol, name in indices.items():
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            price = info.get("regularMarketPrice") or info.get("currentPrice")
            prev_close = info.get("previousClose")

            change = None
            change_pct = None
            if price and prev_close:
                change = round(price - prev_close, 2)
                change_pct = round((change / prev_close) * 100, 2)

            summary.append({
                "symbol": symbol,
                "name": name,
                "price": price,
                "change": change,
                "change_percent": change_pct,
            })
        except Exception:
            summary.append({
                "symbol": symbol,
                "name": name,
                "price": None,
                "error": "Failed to fetch data",
            })

    return {"indices": summary}
