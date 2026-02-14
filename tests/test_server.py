"""Tests for MCP server tool and resource definitions."""

import pytest

from mcptools.server import list_tools, list_resources, list_prompts, call_tool, get_prompt
from unittest.mock import patch


class TestToolDefinitions:
    @pytest.mark.asyncio
    async def test_list_tools_returns_all(self):
        tools = await list_tools()
        names = [t.name for t in tools]
        assert "get_stock_quote" in names
        assert "get_price_history" in names
        assert "get_technical_indicators" in names
        assert "get_financial_news" in names
        assert "get_ticker_news" in names
        assert "get_company_profile" in names
        assert "get_financial_summary" in names

    @pytest.mark.asyncio
    async def test_all_tools_have_schemas(self):
        tools = await list_tools()
        for tool in tools:
            assert tool.inputSchema is not None
            assert "properties" in tool.inputSchema

    @pytest.mark.asyncio
    async def test_call_unknown_tool(self):
        result = await call_tool("nonexistent", {})
        assert "Unknown tool" in result[0].text

    @pytest.mark.asyncio
    @patch("mcptools.server.get_stock_quote")
    async def test_call_stock_quote(self, mock_quote):
        mock_quote.return_value = {"ticker": "AAPL", "price": 195.50}
        result = await call_tool("get_stock_quote", {"ticker": "AAPL"})
        assert "AAPL" in result[0].text
        assert "195.5" in result[0].text


class TestResourceDefinitions:
    @pytest.mark.asyncio
    async def test_list_resources(self):
        resources = await list_resources()
        assert len(resources) >= 1
        uris = [str(r.uri) for r in resources]
        assert "market://summary" in uris


class TestPromptDefinitions:
    @pytest.mark.asyncio
    async def test_list_prompts(self):
        prompts = await list_prompts()
        names = [p.name for p in prompts]
        assert "stock_analysis" in names
        assert "compare_stocks" in names
        assert "market_overview" in names

    @pytest.mark.asyncio
    async def test_get_prompt_stock_analysis(self):
        result = await get_prompt("stock_analysis", {"ticker": "AAPL"})
        assert "AAPL" in result.messages[0].content.text

    @pytest.mark.asyncio
    async def test_get_prompt_compare_stocks(self):
        result = await get_prompt("compare_stocks", {"ticker1": "AAPL", "ticker2": "MSFT"})
        assert "AAPL" in result.messages[0].content.text
        assert "MSFT" in result.messages[0].content.text

    @pytest.mark.asyncio
    async def test_get_unknown_prompt_raises(self):
        with pytest.raises(ValueError, match="Unknown prompt"):
            await get_prompt("nonexistent", {})
