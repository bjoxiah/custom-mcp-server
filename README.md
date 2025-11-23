# Stock Analysis MCP Server

A Model Context Protocol (MCP) server that provides stock market data tools using the Alpha Vantage API. 

## Features

### Tools
- **Company Overview** - Fetch detailed fundamental information about any publicly traded company
- **News Sentiments** - Retrieve market news and sentiment data filtered by tickers or topics
- **Current Stock Price** - Get real-time global quotes for any stock ticker
- **Historical Data** - Access monthly historical stock price data for technical analysis

## Prerequisites

- Python 3.10 or higher
- Poetry (Python package manager)
- Alpha Vantage API key ([Get one free here](https://www.alphavantage.co/support/#api-key))
- Claude Desktop

## Installation

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd custom-mcp-server
```

### 2. Install Dependencies

```bash
poetry install
```

### 3. Configure Environment Variables

Create a `.env` file in the project root:

```env
ALPHA_VANTAGE_BASE_API_URL=https://www.alphavantage.co/query
ALPHA_VANTAGE_KEY=your_api_key_here
```

### 4. Test the Server

```bash
poetry run server
```

If successful, you should see the MCP server start without errors.

## Claude Desktop Configuration

### 1. Locate Your Poetry Virtual Environment

```bash
poetry env info --path
```

This will output something like:
```
/Users/username/Library/Caches/pypoetry/virtualenvs/custom-mcp-server-xxxxx-py3.13
```

### 2. Configure Claude Desktop

Edit your Claude Desktop configuration file:

**MacOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`  
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

Add the following configuration:

```json
{
  "mcpServers": {
    "Stock Analysis": {
      "command": "/path/to/your/virtualenv/custom-mcp-server-xxxxx-py3.13/bin/python",
      "args": ["-m", "custom_mcp_server"],
      "cwd": "/absolute/path/to/custom-mcp-server",
      "env": {
        "ALPHA_VANTAGE_BASE_API_URL": "https://www.alphavantage.co/query",
        "ALPHA_VANTAGE_KEY": "your_api_key_here"
      }
    }
  }
}
```

**Important**: Replace the paths with your actual paths:
- Use the virtualenv path from step 1
- Use the absolute path to your project directory
- The alpha vantage api allows 25 requests per day

### 3. Restart Claude Desktop

Completely quit Claude Desktop (Cmd+Q on Mac) and restart it for the changes to take effect.

## Usage Examples

Once configured, you can interact with the server through Claude Desktop:

### Get Company Information
```
What's the company overview for Apple (AAPL)?
```

### Check Stock Prices
```
What's the current stock price of Tesla?
```

### Analyze Market Sentiment
```
Get news sentiment for Microsoft from the last week
```

### View Historical Data
```
Show me the monthly historical data for Amazon stock
```

## License

MIT License
