#!/usr/bin/env python3
"""
Test script for MCP UJI Academic Server components
"""

import sys
from api_client import create_uji_client
from server import MCPUJIServer

def test_api_client():
    """Test the API client functionality"""
    print("=== Testing UJI API Client ===")
    
    client = create_uji_client()
    
    try:
        # Test subjects
        print("1. Testing subjects endpoint...")
        subjects = client.get_subjects(start=0, limit=3)
        print(f"✓ Retrieved {len(subjects.content)} subjects")
        
        # Test search
        print("2. Testing search functionality...")
        results = client.search_subjects("Matemáticas", "es")
        print(f"✓ Found {len(results)} subjects matching 'Matemáticas'")
        
        # Test degrees
        print("3. Testing degrees endpoint...")
        degrees = client.get_degrees()
        print(f"✓ Retrieved {len(degrees.content)} degrees")
        
        print("✓ API Client tests passed!")
        return True
        
    except Exception as e:
        print(f"✗ API Client test failed: {e}")
        return False
    finally:
        client.close()

def test_server_creation():
    """Test MCP server creation and setup"""
    print("\n=== Testing MCP Server Creation ===")
    
    try:
        server = MCPUJIServer()
        print("✓ MCP Server created successfully")
        
        # Test that server has tools setup
        if hasattr(server, 'server'):
            print("✓ MCP Server has server instance")
        
        server.cleanup()
        print("✓ Server cleanup completed")
        return True
        
    except Exception as e:
        print(f"✗ MCP Server creation failed: {e}")
        return False

def main():
    """Run all tests"""
    print("Testing MCP UJI Academic Server Components\n")
    
    tests_passed = 0
    total_tests = 2
    
    # Test API client
    if test_api_client():
        tests_passed += 1
    
    # Test server creation
    if test_server_creation():
        tests_passed += 1
    
    print(f"\n=== Test Results ===")
    print(f"Tests passed: {tests_passed}/{total_tests}")
    
    if tests_passed == total_tests:
        print("✓ All tests passed! The MCP UJI Academic Server is ready to use.")
        return 0
    else:
        print("✗ Some tests failed. Check the output above for details.")
        return 1

if __name__ == "__main__":
    sys.exit(main())