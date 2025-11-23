import sys
from custom_mcp_server.server import mcp

def main():
    try:
        print("MCP Server starting...", file=sys.stderr, flush=True)
        mcp.run()
    except Exception as e:
        print(f"ERROR: {type(e).__name__}: {e}", file=sys.stderr, flush=True)
        import traceback
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()