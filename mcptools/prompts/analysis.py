"""Financial analysis prompt templates for MCP clients."""

STOCK_ANALYSIS_PROMPT = {
    "name": "stock_analysis",
    "description": "Comprehensive stock analysis with technical and fundamental data",
    "arguments": [
        {"name": "ticker", "description": "Stock ticker symbol", "required": True},
    ],
    "template": """Analyze the stock {ticker} using the available financial data tools.

Please provide:
1. **Company Overview** — What does the company do? Sector and industry.
2. **Current Price Action** — Current price, day range, volume.
3. **Technical Analysis** — Moving averages, RSI, trend direction.
4. **Fundamental Analysis** — P/E ratio, margins, growth metrics, debt levels.
5. **Recent News** — Any recent developments affecting the stock.
6. **Summary** — Bull case, bear case, and overall assessment.

Use the get_stock_quote, get_technical_indicators, get_financial_summary,
get_company_profile, and get_ticker_news tools to gather data.""",
}

COMPARE_STOCKS_PROMPT = {
    "name": "compare_stocks",
    "description": "Compare two stocks on key metrics",
    "arguments": [
        {"name": "ticker1", "description": "First stock ticker", "required": True},
        {"name": "ticker2", "description": "Second stock ticker", "required": True},
    ],
    "template": """Compare {ticker1} and {ticker2} side-by-side.

For each stock, gather:
- Current price and performance
- Key financial metrics (P/E, margins, growth)
- Technical indicators
- Recent news

Then provide a structured comparison table and recommendation
for which stock looks stronger based on the data.""",
}

MARKET_OVERVIEW_PROMPT = {
    "name": "market_overview",
    "description": "Daily market overview and summary",
    "arguments": [],
    "template": """Provide a comprehensive market overview for today.

1. Get market summary for major indices (S&P 500, NASDAQ, Dow Jones).
2. Get top financial news headlines.
3. Summarize the overall market sentiment and key themes.

Use the get_market_summary and get_financial_news tools.""",
}

# Registry of all prompt templates
PROMPT_TEMPLATES = [
    STOCK_ANALYSIS_PROMPT,
    COMPARE_STOCKS_PROMPT,
    MARKET_OVERVIEW_PROMPT,
]
