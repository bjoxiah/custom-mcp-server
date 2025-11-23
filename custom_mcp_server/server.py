import os
import logging
from typing import Optional, Union, Dict
import sys
import httpx
from dotenv import load_dotenv
from fastmcp import FastMCP
from pathlib import Path

from custom_mcp_server.model.company_overview import CompanyOverview
from custom_mcp_server.model.company_sentiment import CompanySentiment
from custom_mcp_server.model.historical_data import HistoricalData
from custom_mcp_server.model.stock_price import StockPrice

# Load environment variables
load_dotenv()
BASE_API_URL = os.getenv("ALPHA_VANTAGE_BASE_API_URL")
API_KEY = os.getenv("ALPHA_VANTAGE_KEY")

print("Server starting...", file=sys.stderr)
print(f"BASE_API_URL: {BASE_API_URL}", file=sys.stderr)
print(f"API_KEY set: {bool(API_KEY)}", file=sys.stderr)

# Get the project root (one level up from this script)
root_dir = Path(__file__).parent.parent
log_file_path = root_dir / "mcp.log"

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    filename=str(log_file_path),  # Convert Path to string
    filemode="a",
)


# Prevent httpx from logging api keys
logging.getLogger("httpx").setLevel(logging.WARNING)

mcp = FastMCP(name="Stock Analysis MCP")


def _format_error_response(exc: Exception, url: str) -> Dict[str, str]:
    """
    Format errors for MCP tools/resources and log them safely.

    Parameters:
        exc (Exception): The exception raised during the HTTP request or parsing.
        url (str): The request URL (API key will be masked).

    Returns:
        dict: Structured error dictionary containing exception type, message, and URL.
    """
    safe_url = url.replace(API_KEY, "***REDACTED***") if API_KEY else url
    logging.error("Request failed: %s | URL: %s", exc, safe_url)
    return {"error": f"{type(exc).__name__}: {str(exc)}", "url": safe_url}


# ---------------------------------------------------------------------------
# Company Overview Tool
# ---------------------------------------------------------------------------
@mcp.tool(
    name="company_overview",
    description="Fetch an overview of a company using its stock ticker symbol.",
)
async def company_overview(ticker: str) -> Union[CompanyOverview, Dict[str, str]]:
    """
    Retrieve detailed fundamental information about a company.

    Parameters:
        ticker (str): Stock ticker symbol (e.g., 'IBM', 'AAPL').

    Returns:
        CompanyOverview: Parsed company overview data.
        OR dict: Structured error dictionary if request fails.
    """
    url = f"{BASE_API_URL}?function=OVERVIEW&symbol={ticker}&apikey={API_KEY}"
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()
            logging.info("Company overview fetched successfully for %s", ticker)
            return CompanyOverview.model_validate(data)
    except (httpx.HTTPStatusError, httpx.RequestError, ValueError) as exc:
        return _format_error_response(exc, url)


# ---------------------------------------------------------------------------
# News Sentiment Tool
# ---------------------------------------------------------------------------
@mcp.tool(
    name="company_sentiment",
    description="Retrieve market news and sentiment data filtered by tickers or topics.",
)
async def company_sentiment(
    tickers: Optional[str] = None,
    topics: Optional[str] = None,
    time_from: Optional[str] = None,
    time_to: Optional[str] = None,
    sort: Optional[str] = None,
    limit: Optional[int] = 20,
) -> Union[CompanySentiment, Dict[str, str]]:
    """
    Fetch market news and sentiment data from Alpha Vantage.

    Parameters:
        tickers (str, optional): Comma-separated tickers.
        topics (str, optional): Comma-separated news topics.
        time_from (str, optional): Start timestamp (YYYYMMDDTHHMM).
        time_to (str, optional): End timestamp (YYYYMMDDTHHMM).
        sort (str, optional): Sort method: LATEST, EARLIEST, RELEVANCE.
        limit (int, optional): Max number of articles (1-1000, default=20).

    Returns:
        CompanySentiment: Parsed sentiment data.
        OR dict: Structured error dictionary if request fails.
    """
    params = {"function": "NEWS_SENTIMENT", "apikey": API_KEY}
    if tickers:
        params["tickers"] = tickers
    if topics:
        params["topics"] = topics
    if time_from:
        params["time_from"] = time_from
    if time_to:
        params["time_to"] = time_to
    if sort:
        params["sort"] = sort
    if limit:
        params["limit"] = limit

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(BASE_API_URL, params=params)
            response.raise_for_status()
            data = response.json()
            logging.info(
                "News sentiment fetched successfully | tickers=%s topics=%s limit=%d",
                tickers, topics, limit
            )
            return CompanySentiment.model_validate(data)
    except (httpx.HTTPStatusError, httpx.RequestError, ValueError) as exc:
        return _format_error_response(exc, BASE_API_URL)


# ---------------------------------------------------------------------------
# Current Stock Price Tool
# ---------------------------------------------------------------------------
@mcp.tool(
    name="get_stock_price",
    description="Retrieve the current global quote (latest stock price) for a ticker.",
)
async def get_stock_price(ticker: str) -> Union[StockPrice, Dict[str, str]]:
    """
    Retrieve the current stock price (GLOBAL_QUOTE) for a company.

    Parameters:
        ticker (str): Stock ticker symbol.

    Returns:
        StockPrice: Parsed global quote data.
        OR dict: Structured error dictionary if request fails.
    """
    url = f"{BASE_API_URL}?function=GLOBAL_QUOTE&symbol={ticker}&apikey={API_KEY}"
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()
            logging.info("Stock price fetched successfully for %s", ticker)
            return StockPrice.model_validate(data)
    except (httpx.HTTPStatusError, httpx.RequestError, ValueError) as exc:
        return _format_error_response(exc, url)


# ---------------------------------------------------------------------------
# Monthly Historical Data Tool
# ---------------------------------------------------------------------------
@mcp.tool(
    name="get_monthly_historical_data",
    description="Fetch monthly historical stock data for a ticker",
)
async def get_monthly_historical(ticker: str) -> Union[HistoricalData, Dict[str, str]]:
    """
    Fetch monthly historical stock data for a ticker.

    Parameters:
        ticker (str): Stock ticker symbol.

    Returns:
        HistoricalData: Parsed monthly time series data.
        OR dict: Structured error dictionary if request fails.
    """
    url = f"{BASE_API_URL}?function=TIME_SERIES_MONTHLY&symbol={ticker}&apikey={API_KEY}"
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()
            logging.info("Monthly historical data fetched successfully for %s", ticker)
            return HistoricalData.model_validate(data)
    except (httpx.HTTPStatusError, httpx.RequestError, ValueError) as exc:
        return _format_error_response(exc, url)
    
    


# At the bottom of server.py, modify how mcp runs:
if __name__ == "__main__":
    import sys
    print("Starting MCP server...", file=sys.stderr)
    mcp.run(transport="stdio") 
