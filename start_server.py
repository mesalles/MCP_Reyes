#!/usr/bin/env python3
"""
MCP UJI Academic Server Launcher
Allows starting the server in local (stdio) or remote (HTTP/WebSocket) mode
"""

import argparse
import asyncio
import subprocess
import sys
import os
from pathlib import Path


def main():
    """Main launcher function"""
    parser = argparse.ArgumentParser(
        description="MCP UJI Academic Server - Launch in local or remote mode",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Start local server (for Claude Desktop local configuration)
  python start_server.py --mode local
  
  # Start remote server accessible from network
  python start_server.py --mode remote --host 0.0.0.0 --port 8000
  
  # Start remote server on localhost only
  python start_server.py --mode remote --host 127.0.0.1 --port 8000
        """
    )
    
    parser.add_argument(
        "--mode", 
        choices=["local", "remote"], 
        default="local",
        help="Server mode: 'local' for stdio (Claude Desktop), 'remote' for HTTP/WebSocket"
    )
    
    parser.add_argument(
        "--host", 
        default="127.0.0.1", 
        help="Host address for remote mode (default: 127.0.0.1)"
    )
    
    parser.add_argument(
        "--port", 
        type=int, 
        default=8000, 
        help="Port number for remote mode (default: 8000)"
    )
    
    parser.add_argument(
        "--reload", 
        action="store_true", 
        help="Enable auto-reload for development (remote mode only)"
    )
    
    args = parser.parse_args()
    
    # Get the directory where this script is located
    script_dir = Path(__file__).parent.absolute()
    
    if args.mode == "local":
        print("🚀 Starting MCP UJI Academic Server in LOCAL mode (stdio)")
        print("📋 This mode is for Claude Desktop local configuration")
        print("⚙️  Use this server configuration in Claude Desktop:")
        print(f"   Command: uv run {script_dir}/server.py")
        print()
        
        # Run the local stdio server
        server_path = script_dir / "server.py"
        try:
            subprocess.run([sys.executable, str(server_path)], cwd=script_dir)
        except KeyboardInterrupt:
            print("\n🛑 Server stopped by user")
        except Exception as e:
            print(f"❌ Error running local server: {e}")
            sys.exit(1)
    
    elif args.mode == "remote":
        print("🚀 Starting MCP UJI Academic Server in REMOTE mode (HTTP/WebSocket)")
        print(f"🌐 Server will be accessible at: http://{args.host}:{args.port}")
        print(f"🔌 WebSocket endpoint: ws://{args.host}:{args.port}/ws/{{client_id}}")
        print("📋 Configure Claude Desktop to connect to this remote server")
        print()
        
        # Run the remote HTTP/WebSocket server
        remote_server_path = script_dir / "remote_server.py"
        
        cmd = [
            sys.executable, str(remote_server_path),
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
            print(f"❌ Error running remote server: {e}")
            sys.exit(1)


if __name__ == "__main__":
    main()