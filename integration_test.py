#!/usr/bin/env python3
"""
Integration test to verify MCP server is working correctly
"""

import json
import subprocess
import asyncio
import time

def test_server_startup():
    """Test that the server starts without errors"""
    print("Testing MCP UJI Academic Server startup...")
    
    try:
        # Start the server process
        process = subprocess.Popen(
            ["uv", "run", "main.py"],
            cwd="/home/al419150/investigation_work/lsi_work/semanticbots_solutai/MCP_UJI_academic",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Let it run for a few seconds
        time.sleep(3)
        
        # Check if process is still running (no immediate crash)
        if process.poll() is None:
            print("✓ Server started successfully and is running")
            process.terminate()
            process.wait(timeout=5)
            return True
        else:
            stdout, stderr = process.communicate()
            print("✗ Server crashed on startup")
            print(f"STDOUT: {stdout}")
            print(f"STDERR: {stderr}")
            return False
            
    except Exception as e:
        print(f"✗ Failed to test server startup: {e}")
        return False

def test_components():
    """Test that all components work correctly"""
    print("\nTesting individual components...")
    
    try:
        # Test that we can import all modules
        from api_client import create_uji_client
        from server import MCPUJIServer
        from models import Subject, Degree, Location
        
        print("✓ All modules imported successfully")
        
        # Test API client creation
        client = create_uji_client()
        client.close()
        print("✓ API client created and closed successfully")
        
        # Test server creation
        server = MCPUJIServer()
        server.cleanup()
        print("✓ MCP server created and cleaned up successfully")
        
        return True
        
    except Exception as e:
        print(f"✗ Component test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("MCP UJI Academic Server - Integration Tests")
    print("=" * 50)
    
    tests_passed = 0
    total_tests = 2
    
    # Test component imports and creation
    if test_components():
        tests_passed += 1
    
    # Test server startup
    if test_server_startup():
        tests_passed += 1
    
    print(f"\n{'=' * 50}")
    print(f"Integration Test Results: {tests_passed}/{total_tests} passed")
    
    if tests_passed == total_tests:
        print("🎉 All integration tests passed!")
        print("\nThe MCP UJI Academic Server is ready for production use.")
        print("\nTo use the server, add it to your MCP client configuration:")
        print('```json')
        print('{')
        print('  "mcpServers": {')
        print('    "mcp-uji-academic": {')
        print('      "command": "uv",')
        print('      "args": ["run", "/path/to/MCP_UJI_academic/main.py"],')
        print('      "cwd": "/path/to/MCP_UJI_academic"')
        print('    }')
        print('  }')
        print('}')
        print('```')
        return 0
    else:
        print("❌ Some integration tests failed.")
        return 1

if __name__ == "__main__":
    exit(main())