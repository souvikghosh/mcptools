# mcptools

**An MCP server that gives Claude and any MCP-compatible AI client live access to financial markets data.**

Plug it into Claude Desktop in two minutes — then ask Claude to analyze a stock, pull earnings metrics, or summarize market news without copy-pasting a single number.

```bash
pip install mcptools
```

```json
// claude_desktop_config.json
{
  "mcpServers": {
    "mcptools": {
      "command": "python",
      "args": ["-m", "mcptools.server"]
    }
  }
}
```

---

## Tools

Seven tools exposed over MCP stdio transport:

| Tool | What it returns |
|---|---|
| `get_stock_quote` | Real-time price, volume, day high/low |
| `get_historical_prices` | OHLCV data with configurable period and interval |
| `get_technical_indicators` | SMA, RSI, trend signals |
| `get_financial_news` | Top market headlines from RSS feeds |
| `get_ticker_news` | News articles for a specific ticker |
| `get_company_profile` | Sector, industry, employee count |
| `get_financial_summary` | Revenue, margins, P/E ratio, debt, cash flow |

## Resources

- `market://summary` — live snapshot of major market indices as JSON

---

## Quick start

```bash
# install
pip install mcptools

# configure Claude Desktop (copy example config)
cp examples/claude_desktop_config.json ~/Library/Application\ Support/Claude/claude_desktop_config.json

# or run directly
python -m mcptools.server
```

Copy `.env.example` to `.env` for any environment configuration.

---

## Example prompts (in Claude Desktop)

```
"What is NVDA trading at right now and how does its P/E compare to the sector?"
"Summarize this week's market news and flag anything moving the S&P."
"Pull AAPL's RSI and SMA-20 and tell me if it's overbought."
```

---

## Architecture

```
mcptools/
├── tools/
│   ├── stocks.py       # quote and historical price tools
│   ├── news.py         # market and ticker news tools
│   └── company.py      # profile and financial summary tools
├── resources/          # market://summary resource
├── prompts/            # reusable analysis prompt templates
├── server.py           # MCP server entry point, tool routing
└── config.py           # settings via .env
```

Built on the official [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk) with stdio transport. Tool routing uses a dispatch dictionary with async support throughout.

---

## Stack

Python · MCP SDK · yfinance · feedparser · Pydantic · Docker
