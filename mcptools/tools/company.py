"""Company profile and financial data tools."""

import yfinance as yf


def get_company_profile(ticker: str) -> dict:
    """Get detailed company profile information.

    Returns business description, sector, industry, key executives, and more.
    """
    stock = yf.Ticker(ticker)
    info = stock.info

    return {
        "ticker": ticker.upper(),
        "name": info.get("shortName", "N/A"),
        "long_name": info.get("longName", "N/A"),
        "sector": info.get("sector", "N/A"),
        "industry": info.get("industry", "N/A"),
        "description": info.get("longBusinessSummary", "N/A"),
        "website": info.get("website", "N/A"),
        "country": info.get("country", "N/A"),
        "city": info.get("city", "N/A"),
        "employees": info.get("fullTimeEmployees"),
        "exchange": info.get("exchange", "N/A"),
    }


def get_financial_summary(ticker: str) -> dict:
    """Get key financial metrics for a company.

    Returns revenue, earnings, margins, debt metrics, and valuation ratios.
    """
    stock = yf.Ticker(ticker)
    info = stock.info

    return {
        "ticker": ticker.upper(),
        "name": info.get("shortName", "N/A"),
        "market_cap": info.get("marketCap"),
        "enterprise_value": info.get("enterpriseValue"),
        "revenue": info.get("totalRevenue"),
        "revenue_growth": info.get("revenueGrowth"),
        "gross_margins": info.get("grossMargins"),
        "operating_margins": info.get("operatingMargins"),
        "profit_margins": info.get("profitMargins"),
        "earnings_per_share": info.get("trailingEps"),
        "pe_ratio": info.get("trailingPE"),
        "forward_pe": info.get("forwardPE"),
        "peg_ratio": info.get("pegRatio"),
        "price_to_book": info.get("priceToBook"),
        "debt_to_equity": info.get("debtToEquity"),
        "return_on_equity": info.get("returnOnEquity"),
        "free_cash_flow": info.get("freeCashflow"),
        "dividend_yield": info.get("dividendYield"),
    }
