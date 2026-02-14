"""MCP server entry point — exposes financial data tools via Model Context Protocol."""

import json

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    Tool,
    TextContent,
    Resource,
    ResourceTemplate,
    Prompt,
    PromptArgument,
    PromptMessage,
    GetPromptResult,
)

from mcptools.tools.stocks import get_stock_quote, get_price_history, get_technical_indicators
from mcptools.tools.news import get_financial_news, get_ticker_news
from mcptools.tools.company import get_company_profile, get_financial_summary
from mcptools.resources.market import get_market_summary
from mcptools.prompts.analysis import PROMPT_TEMPLATES

# Create the MCP server
server = Server("mcptools")


# --- Tool definitions ---

@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="get_stock_quote",
            description="Get current stock quote with price, volume, and key metrics",
            inputSchema={
                "type": "object",
                "properties": {
                    "ticker": {"type": "string", "description": "Stock ticker symbol (e.g., AAPL)"},
                },
                "required": ["ticker"],
            },
        ),
        Tool(
            name="get_price_history",
            description="Get historical price data for a stock",
            inputSchema={
                "type": "object",
                "properties": {
                    "ticker": {"type": "string", "description": "Stock ticker symbol"},
                    "period": {
                        "type": "string",
                        "description": "Time period: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, max",
                        "default": "1mo",
                    },
                    "interval": {
                        "type": "string",
                        "description": "Data interval: 1m, 5m, 15m, 1h, 1d, 1wk, 1mo",
                        "default": "1d",
                    },
                },
                "required": ["ticker"],
            },
        ),
        Tool(
            name="get_technical_indicators",
            description="Calculate technical indicators: SMA(20/50/200), RSI(14), trend signals",
            inputSchema={
                "type": "object",
                "properties": {
                    "ticker": {"type": "string", "description": "Stock ticker symbol"},
                },
                "required": ["ticker"],
            },
        ),
        Tool(
            name="get_financial_news",
            description="Get latest financial news headlines, optionally filtered by query",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Optional search query"},
                    "max_results": {"type": "integer", "description": "Max articles", "default": 10},
                },
            },
        ),
        Tool(
            name="get_ticker_news",
            description="Get news articles about a specific stock ticker",
            inputSchema={
                "type": "object",
                "properties": {
                    "ticker": {"type": "string", "description": "Stock ticker symbol"},
                    "max_results": {"type": "integer", "description": "Max articles", "default": 5},
                },
                "required": ["ticker"],
            },
        ),
        Tool(
            name="get_company_profile",
            description="Get company profile: sector, industry, description, employees",
            inputSchema={
                "type": "object",
                "properties": {
                    "ticker": {"type": "string", "description": "Stock ticker symbol"},
                },
                "required": ["ticker"],
            },
        ),
        Tool(
            name="get_financial_summary",
            description="Get key financial metrics: revenue, margins, P/E, debt, cash flow",
            inputSchema={
                "type": "object",
                "properties": {
                    "ticker": {"type": "string", "description": "Stock ticker symbol"},
                },
                "required": ["ticker"],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Route tool calls to the appropriate handler."""
    handlers = {
        "get_stock_quote": lambda args: get_stock_quote(args["ticker"]),
        "get_price_history": lambda args: get_price_history(
            args["ticker"], args.get("period", "1mo"), args.get("interval", "1d")
        ),
        "get_technical_indicators": lambda args: get_technical_indicators(args["ticker"]),
        "get_financial_news": lambda args: get_financial_news(
            args.get("query"), args.get("max_results", 10)
        ),
        "get_ticker_news": lambda args: get_ticker_news(
            args["ticker"], args.get("max_results", 5)
        ),
        "get_company_profile": lambda args: get_company_profile(args["ticker"]),
        "get_financial_summary": lambda args: get_financial_summary(args["ticker"]),
    }

    handler = handlers.get(name)
    if not handler:
        return [TextContent(type="text", text=f"Unknown tool: {name}")]

    try:
        result = handler(arguments)
        # Handle async functions
        if hasattr(result, "__await__"):
            result = await result
        return [TextContent(type="text", text=json.dumps(result, indent=2, default=str))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


# --- Resource definitions ---

@server.list_resources()
async def list_resources() -> list[Resource]:
    return [
        Resource(
            uri="market://summary",
            name="Market Summary",
            description="Current major market indices overview",
            mimeType="application/json",
        ),
    ]


@server.read_resource()
async def read_resource(uri: str) -> str:
    if str(uri) == "market://summary":
        result = get_market_summary()
        return json.dumps(result, indent=2, default=str)
    raise ValueError(f"Unknown resource: {uri}")


# --- Prompt definitions ---

@server.list_prompts()
async def list_prompts() -> list[Prompt]:
    return [
        Prompt(
            name=p["name"],
            description=p["description"],
            arguments=[
                PromptArgument(name=a["name"], description=a["description"], required=a["required"])
                for a in p.get("arguments", [])
            ],
        )
        for p in PROMPT_TEMPLATES
    ]


@server.get_prompt()
async def get_prompt(name: str, arguments: dict | None = None) -> GetPromptResult:
    template = next((p for p in PROMPT_TEMPLATES if p["name"] == name), None)
    if not template:
        raise ValueError(f"Unknown prompt: {name}")

    arguments = arguments or {}
    text = template["template"].format(**arguments)

    return GetPromptResult(
        description=template["description"],
        messages=[
            PromptMessage(role="user", content=TextContent(type="text", text=text))
        ],
    )


# --- Server entry point ---

async def main():
    """Run the MCP server on stdio transport."""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
