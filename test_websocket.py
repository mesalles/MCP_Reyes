#!/usr/bin/env python3
"""
Test script for MCP UJI Academic WebSocket server
"""

import asyncio
import json
import websockets

async def test_websocket():
    """Test WebSocket connection to MCP server"""
    uri = "ws://localhost:8084/ws/test-client"
    
    try:
        print("🔌 Connecting to WebSocket server...")
        async with websockets.connect(uri) as websocket:
            print("✅ Connected successfully!")
            
            # Test 1: List tools
            print("\n📋 Testing tools/list...")
            request = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "tools/list"
            }
            
            await websocket.send(json.dumps(request))
            response = await websocket.recv()
            result = json.loads(response)
            
            print(f"✅ Found {len(result.get('result', {}).get('tools', []))} tools")
            for tool in result.get('result', {}).get('tools', []):
                print(f"  - {tool['name']}: {tool['description']}")
            
            # Test 2: Call a tool (get_subjects)
            print("\n📚 Testing tools/call - get_subjects...")
            request = {
                "jsonrpc": "2.0", 
                "id": 2,
                "method": "tools/call",
                "params": {
                    "name": "get_subjects",
                    "arguments": {
                        "limit": 3,
                        "full": False
                    }
                }
            }
            
            await websocket.send(json.dumps(request))
            response = await websocket.recv()
            result = json.loads(response)
            
            if 'result' in result:
                print("✅ get_subjects call successful!")
                content = result['result']['content'][0]['text']
                subjects_data = json.loads(content)
                print(f"Found {subjects_data.get('total_subjects', 0)} subjects")
            else:
                print(f"❌ Tool call failed: {result}")
            
            # Test 3: Search subjects
            print("\n🔍 Testing tools/call - search_subjects...")
            request = {
                "jsonrpc": "2.0",
                "id": 3, 
                "method": "tools/call",
                "params": {
                    "name": "search_subjects",
                    "arguments": {
                        "query": "Matemáticas",
                        "language": "es"
                    }
                }
            }
            
            await websocket.send(json.dumps(request))
            response = await websocket.recv()
            result = json.loads(response)
            
            if 'result' in result:
                print("✅ search_subjects call successful!")
                content = result['result']['content'][0]['text']
                search_data = json.loads(content)
                print(f"Found {search_data.get('total_results', 0)} results for 'Matemáticas'")
            else:
                print(f"❌ Search failed: {result}")
                
    except Exception as e:
        print(f"❌ Connection failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_websocket())