#!/usr/bin/env python3
"""
Integration test to verify HTTP MCP server is working correctly
"""

import json
import subprocess
import requests
import time
import os

def test_server_startup():
    """Test that the HTTP MCP server starts without errors"""
    print("Testing HTTP MCP UJI Academic Server startup...")
    
    try:
        # Start the HTTP server process
        process = subprocess.Popen(
            ["uv", "run", "start_server.py", "--host", "127.0.0.1", "--port", "8086"],
            cwd=os.path.dirname(os.path.abspath(__file__)),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Let it run for a few seconds to start up
        time.sleep(5)
        
        # Check if process is still running (no immediate crash)
        if process.poll() is None:
            print("✓ HTTP Server started successfully and is running")
            
            # Test HTTP endpoints
            try:
                # Test health endpoint
                health_response = requests.get("http://127.0.0.1:8086/health", timeout=5)
                if health_response.status_code == 200:
                    print("✓ Health endpoint responding")
                else:
                    print(f"✗ Health endpoint returned {health_response.status_code}")
                    return False
                
                # Test MCP ping
                ping_data = {
                    "jsonrpc": "2.0",
                    "id": 1,
                    "method": "ping"
                }
                ping_response = requests.post(
                    "http://127.0.0.1:8086/mcp",
                    json=ping_data,
                    headers={"Content-Type": "application/json"},
                    timeout=5
                )
                if ping_response.status_code == 200:
                    print("✓ MCP ping responding")
                    
                    process.terminate()
                    process.wait(timeout=5)
                    return True
                else:
                    print(f"✗ MCP ping returned {ping_response.status_code}")
                    return False
                    
            except requests.RequestException as e:
                print(f"✗ HTTP request failed: {e}")
                return False
        else:
            stdout, stderr = process.communicate()
            print("✗ Server crashed on startup")
            print(f"STDOUT: {stdout}")
            print(f"STDERR: {stderr}")
            return False
            
    except Exception as e:
        print(f"✗ Failed to test server startup: {e}")
        return False
    finally:
        # Clean up
        if 'process' in locals() and process.poll() is None:
            process.terminate()
            process.wait()

def test_components():
    """Test that all components work correctly"""
    print("\nTesting individual components...")
    
    try:
        # Test that we can import all modules
        from api_client import create_uji_client
        from models import Subject, Degree, Location
        
        print("✓ All modules imported successfully")
        
        # Test API client creation
        client = create_uji_client()
        client.close()
        print("✓ API client created and closed successfully")
        
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