#!/usr/bin/env python3
"""
MCP UJI Academic HTTP Server Lau    print("� Compatible with MCP Inspector (Streamable HTTP)")
    print()
    
    # Run the HTTP MCP server
    mcp_server_path = script_dir / "mcp_server.py"
    
    cmd = [
        sys.executable, str(mcp_server_path),
        "--host", args.host,
        "--port", str(args.port)
    ]ified launcher for HTTP-only MCP server
"""

import argparse
import asyncio
import subprocess
import sys
import os
from pathlib import Path


def main():
    """Main launcher function - HTTP MCP Server only"""
    parser = argparse.ArgumentParser(
        description="MCP UJI Academic HTTP Server",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Start server on localhost (development)
  python start_server.py --host 127.0.0.1 --port 8084
  
  # Start server accessible from network
  python start_server.py --host 0.0.0.0 --port 8084
  
  # Start with auto-reload for development
  python start_server.py --host 127.0.0.1 --port 8084 --reload
        """
    )
    
    parser.add_argument(
        "--host", 
        default="127.0.0.1", 
        help="Host address to bind to (default: 127.0.0.1)"
    )
    
    parser.add_argument(
        "--port", 
        type=int, 
        default=8084, 
        help="Port number to bind to (default: 8084)"
    )
    
    parser.add_argument(
        "--reload", 
        action="store_true", 
        help="Enable auto-reload for development"
    )
    
    args = parser.parse_args()
    
    # Get the directory where this script is located
    script_dir = Path(__file__).parent.absolute()
    
    print("🚀 Starting MCP UJI Academic HTTP Server")
    print(f"🌐 Server will be accessible at: http://{args.host}:{args.port}")
    print(f"🔌 MCP Endpoint: http://{args.host}:{args.port}/mcp")
    print("� Compatible with MCP Inspector (Streamable HTTP)")
    print()
    
    # Run the HTTP MCP server
    mcp_server_path = script_dir / "mcp_server.py"
    
    cmd = [
        sys.executable, str(mcp_server_path),
        "--host", args.host,
        "--port", str(args.port)
    ]
    
    if args.reload:
        cmd.append("--reload")
    
    try:
        subprocess.run(cmd, cwd=script_dir)
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Error running HTTP server: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()