# test_server.py
import asyncio
from fastmcp import Client
from .server import mcp

async def test_tools():
    client = Client(mcp)
    
    async with client:
        # Test tool call
        result = await client.call_tool(
            "company_overview",
            {"ticker": 'AAPL'}
        )
        print(f"Addition result: {result}")
        
        # Test resource fetch
        # historical = await client.read_resource(
        #     "stock://AAPL/historical"
        # )
        # print(f"Stock Historical Data: {historical}")


def main():
    asyncio.run(test_tools())
    
if __name__ == "__main__":
    asyncio.run(test_tools())
