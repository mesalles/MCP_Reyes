# %% Main Entry Point
## Entry point for the MCP UJI Academic Server

import asyncio
import sys
from server import main as server_main


def main():
    """Main entry point for the MCP UJI Academic Server"""
    try:
        # Run the MCP server
        asyncio.run(server_main())
    except KeyboardInterrupt:
        print("Server interrupted by user", file=sys.stderr)
        sys.exit(0)
    except Exception as e:
        print(f"Server error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
