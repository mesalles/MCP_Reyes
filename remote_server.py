# %% HTTP MCP Server
## HTTP-only server for MCP access

import asyncio
import json
import logging
import argparse
import os
from typing import Dict, Any, Optional
from contextlib import asynccontextmanager

# FastAPI imports  
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Local imports
from api_client import UJIAcademicClient, create_uji_client
from models import (
    Subject, Degree, Location, ScheduleEvent, APIError,
    SubjectsResponse, DegreesResponse, LocationsResponse, ScheduleResponse
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global server instance
mcp_server_instance = None


# %% HTTP MCP Server
## Simple HTTP-only MCP server implementation


# %% HTTP MCP Server Implementation
## Simplified server with only HTTP support

class HTTPMCPServer:
    """HTTP-only MCP Server"""
    
    def __init__(self):
        self.client: Optional[UJIAcademicClient] = None
    
    def cleanup(self):
        """Cleanup resources"""
        if self.client:
            self.client.close()
            logger.info("API client closed")
# %% FastAPI Application
## FastAPI application for remote MCP access

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    global mcp_server_instance
    
    # Startup
    logger.info("Starting HTTP MCP UJI Academic Server...")
    mcp_server_instance = HTTPMCPServer()
    
    yield
    
    # Shutdown
    if mcp_server_instance:
        mcp_server_instance.cleanup()
    logger.info("HTTP MCP UJI Academic Server stopped")


# Create FastAPI app
app = FastAPI(
    title="MCP UJI Academic Server",
    description="Remote access to Universitat Jaume I academic information via MCP",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# HTTP-only server - no connection manager needed


# %% HTTP Endpoints
## REST API endpoints for testing and info

@app.get("/")
async def root():
    """Root endpoint with server information"""
    return {
        "name": "MCP UJI Academic Server",
        "version": "1.0.0",
        "description": "HTTP-only access to UJI academic information via MCP protocol",
        "endpoints": {
            "mcp": "/mcp (POST for MCP protocol)",
            "health": "/health",
            "tools": "/tools"
        },
        "transport": "HTTP only"
    }

@app.post("/mcp")
async def mcp_endpoint(request: dict):
    """MCP HTTP endpoint for Inspector compatibility"""
    if not mcp_server_instance:
        raise HTTPException(status_code=503, detail="MCP server not ready")
    
    try:
        method = request.get("method")
        request_id = request.get("id")
        params = request.get("params", {})
        
        logger.info(f"MCP HTTP request: {method}")
        
        if method == "initialize":
            # Initialize response
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {
                        "tools": {
                            "listChanged": False
                        },
                        "resources": {
                            "subscribe": False,
                            "listChanged": False
                        }
                    },
                    "serverInfo": {
                        "name": "mcp-uji-academic",
                        "version": "1.0.0"
                    }
                }
            }
        
        elif method == "ping":
            # Ping response - simple acknowledgment
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {}
            }
        
        elif method == "tools/list":
            # List tools - return hardcoded list since we can't access MCP internals
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "tools": [
                        {
                            "name": "get_subjects",
                            "description": "Get list of subjects with pagination support. Returns subjects from UJI academic system.",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "start": {"type": "integer", "description": "Starting record number (default: 0)", "default": 0},
                                    "limit": {"type": "integer", "description": "Number of records to return (default: 20, max: 100)", "default": 20, "maximum": 100},
                                    "full": {"type": "boolean", "description": "Return full subject details (default: false)", "default": False}
                                }
                            }
                        },
                        {
                            "name": "search_subjects",
                            "description": "Search subjects by name or ID with language preference",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "query": {"type": "string", "description": "Search query (subject name or ID)"},
                                    "language": {"type": "string", "description": "Language preference (ca, es, en)", "enum": ["ca", "es", "en"], "default": "es"}
                                },
                                "required": ["query"]
                            }
                        },
                        {
                            "name": "get_degrees",
                            "description": "Get list of all degree programs from UJI",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "full": {"type": "boolean", "description": "Return full degree details (default: true)", "default": True}
                                }
                            }
                        },
                        {
                            "name": "search_degrees", 
                            "description": "Search degree programs by name with language preference",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "query": {"type": "string", "description": "Search query (degree name)"},
                                    "language": {"type": "string", "description": "Language preference (ca, es, en)", "enum": ["ca", "es", "en"], "default": "es"}
                                },
                                "required": ["query"]
                            }
                        },
                        {
                            "name": "get_locations",
                            "description": "Get list of all university locations (buildings, classrooms, labs)",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "full": {"type": "boolean", "description": "Return full location details (default: true)", "default": True}
                                }
                            }
                        },
                        {
                            "name": "search_locations",
                            "description": "Search university locations by building name or description",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "query": {"type": "string", "description": "Search query (building name or location description)"}
                                },
                                "required": ["query"]
                            }
                        },
                        {
                            "name": "get_class_schedule",
                            "description": "Get class schedule for a degree program in a specific year",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "year": {"type": "string", "description": "Academic year (e.g., '2025')"},
                                    "degree_id": {"type": "string", "description": "Degree program identifier (e.g., '208')"}
                                },
                                "required": ["year", "degree_id"]
                            }
                        },
                        {
                            "name": "get_exam_schedule",
                            "description": "Get exam schedule for a degree program in a specific year",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "year": {"type": "string", "description": "Academic year (e.g., '2025')"},
                                    "degree_id": {"type": "string", "description": "Degree program identifier (e.g., '208')"}
                                },
                                "required": ["year", "degree_id"]
                            }
                        }
                    ]
                }
            }
        
        elif method == "tools/call":
            # Call tool - execute tool logic directly
            tool_name = params.get("name")
            arguments = params.get("arguments", {})
            
            # Initialize client if needed
            if not mcp_server_instance.client:
                mcp_server_instance.client = create_uji_client()
            
            try:
                # Execute tool logic directly (same as in RemoteMCPServer.setup_tools)
                if tool_name == "get_subjects":
                    start = arguments.get("start", 0)
                    limit = min(arguments.get("limit", 20), 100)
                    full = arguments.get("full", False)
                    response = mcp_server_instance.client.get_subjects(start=start, limit=limit, full=full)
                    result_text = json.dumps({
                        "subjects": [subject.model_dump() for subject in response.content],
                        "pagination": response.page.model_dump() if response.page else None,
                        "total_subjects": len(response.content)
                    }, indent=2, ensure_ascii=False)
                
                elif tool_name == "search_subjects":
                    query = arguments["query"]
                    language = arguments.get("language", "es")
                    subjects = mcp_server_instance.client.search_subjects(query, language)
                    result_text = json.dumps({
                        "query": query,
                        "language": language,
                        "results": [subject.model_dump() for subject in subjects],
                        "total_results": len(subjects)
                    }, indent=2, ensure_ascii=False)
                
                elif tool_name == "get_degrees":
                    full = arguments.get("full", True)
                    response = mcp_server_instance.client.get_degrees(full=full)
                    result_text = json.dumps({
                        "degrees": [degree.model_dump() for degree in response.content],
                        "total_degrees": len(response.content)
                    }, indent=2, ensure_ascii=False)
                
                elif tool_name == "search_degrees":
                    query = arguments["query"]
                    language = arguments.get("language", "es")
                    degrees = mcp_server_instance.client.search_degrees(query, language)
                    result_text = json.dumps({
                        "query": query,
                        "language": language,
                        "results": [degree.model_dump() for degree in degrees],
                        "total_results": len(degrees)
                    }, indent=2, ensure_ascii=False)
                
                elif tool_name == "get_locations":
                    full = arguments.get("full", True)
                    response = mcp_server_instance.client.get_locations(full=full)
                    result_text = json.dumps({
                        "locations": [location.model_dump() for location in response.content],
                        "total_locations": len(response.content)
                    }, indent=2, ensure_ascii=False)
                
                elif tool_name == "search_locations":
                    query = arguments["query"]
                    locations = mcp_server_instance.client.search_locations(query)
                    result_text = json.dumps({
                        "query": query,
                        "results": [location.model_dump() for location in locations],
                        "total_results": len(locations)
                    }, indent=2, ensure_ascii=False)
                
                elif tool_name == "get_class_schedule":
                    year = arguments["year"]
                    degree_id = arguments["degree_id"]
                    response = mcp_server_instance.client.get_class_schedule(year, degree_id)
                    result_text = json.dumps({
                        "year": year,
                        "degree_id": degree_id,
                        "schedule": response.model_dump(),
                        "summary": {
                            "total_events": response.total_events,
                            "date_range": response.date_range
                        }
                    }, indent=2, ensure_ascii=False, default=str)
                
                elif tool_name == "get_exam_schedule":
                    year = arguments["year"]
                    degree_id = arguments["degree_id"]
                    response = mcp_server_instance.client.get_exam_schedule(year, degree_id)
                    result_text = json.dumps({
                        "year": year,
                        "degree_id": degree_id,
                        "exam_schedule": response.model_dump(),
                        "summary": {
                            "total_exams": response.total_events,
                            "date_range": response.date_range
                        }
                    }, indent=2, ensure_ascii=False, default=str)
                
                else:
                    result_text = json.dumps({"error": "Unknown tool", "tool_name": tool_name}, indent=2)
                
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "content": [
                            {
                                "type": "text",
                                "text": result_text
                            }
                        ]
                    }
                }
            
            except Exception as e:
                logger.error(f"Tool execution error: {e}")
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {
                        "code": -32603,
                        "message": f"Tool execution error: {str(e)}"
                    }
                }
        
        elif method == "resources/list":
            # List resources - return hardcoded list
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "resources": [
                        {
                            "uri": "uji://api/info",
                            "name": "UJI Academic API Information",
                            "description": "Information about UJI Academic API endpoints and usage",
                            "mimeType": "application/json"
                        }
                    ]
                }
            }
        
        elif method == "resources/read":
            # Read resource - execute logic directly
            uri = params.get("uri")
            if uri == "uji://api/info":
                content = json.dumps({
                    "name": "UJI Academic Information System API",
                    "description": "Access to Universitat Jaume I academic data",
                    "version": "1.0.0",
                    "remote_access": True,
                    "endpoints": {
                        "subjects": "Subject information and management",
                        "degrees": "Degree program information", 
                        "schedules": "Class and exam schedules",
                        "locations": "University location information"
                    }
                }, indent=2)
            else:
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {
                        "code": -32602,
                        "message": f"Unknown resource: {uri}"
                    }
                }
            
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "contents": [
                        {
                            "uri": uri,
                            "mimeType": "application/json",
                            "text": content
                        }
                    ]
                }
            }
        
        elif method == "resources/templates/list":
            # List templates - return empty list since we don't have templates
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "resourceTemplates": []
                }
            }
        
        elif method == "prompts/list":
            # List prompts - return empty list since we don't have prompts
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "prompts": []
                }
            }
        
        else:
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {
                    "code": -32601,
                    "message": f"Method not found: {method}"
                }
            }
    
    except Exception as e:
        logger.error(f"MCP HTTP error: {e}")
        return {
            "jsonrpc": "2.0",
            "id": request.get("id"),
            "error": {
                "code": -32603,
                "message": f"Internal error: {str(e)}"
            }
        }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "server": "mcp-uji-academic",
        "timestamp": asyncio.get_event_loop().time()
    }

@app.get("/tools")
async def list_tools():
    """List available MCP tools"""
    if not mcp_server_instance:
        raise HTTPException(status_code=503, detail="MCP server not ready")
    
    # Return hardcoded list of tools since we can't access internal MCP handlers
    return {
        "tools": [
            {
                "name": "get_subjects",
                "description": "Get list of subjects with pagination support",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "start": {"type": "integer", "description": "Starting record number", "default": 0},
                        "limit": {"type": "integer", "description": "Number of records to return", "default": 20},
                        "full": {"type": "boolean", "description": "Return full subject details", "default": False}
                    }
                }
            },
            {
                "name": "search_subjects",
                "description": "Search subjects by name or ID",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Search query"},
                        "language": {"type": "string", "enum": ["ca", "es", "en"], "default": "es"}
                    },
                    "required": ["query"]
                }
            },
            {
                "name": "get_degrees", 
                "description": "Get list of degree programs",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "full": {"type": "boolean", "description": "Return full details", "default": True}
                    }
                }
            },
            {
                "name": "search_degrees",
                "description": "Search degree programs by name", 
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Search query"},
                        "language": {"type": "string", "enum": ["ca", "es", "en"], "default": "es"}
                    },
                    "required": ["query"]
                }
            },
            {
                "name": "get_locations",
                "description": "Get university locations",
                "inputSchema": {
                    "type": "object", 
                    "properties": {
                        "full": {"type": "boolean", "description": "Return full details", "default": True}
                    }
                }
            },
            {
                "name": "search_locations",
                "description": "Search university locations",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Search query"}
                    },
                    "required": ["query"]
                }
            },
            {
                "name": "get_class_schedule",
                "description": "Get class schedule for a degree",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "year": {"type": "string", "description": "Academic year"},
                        "degree_id": {"type": "string", "description": "Degree ID"}
                    },
                    "required": ["year", "degree_id"]
                }
            },
            {
                "name": "get_exam_schedule", 
                "description": "Get exam schedule for a degree",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "year": {"type": "string", "description": "Academic year"},
                        "degree_id": {"type": "string", "description": "Degree ID"}
                    },
                    "required": ["year", "degree_id"] 
                }
            }
        ]
    }


# %% HTTP Only - WebSocket support removed


# %% Main Entry Point
## Main function to run the remote server

def main():
    """Main entry point for HTTP MCP server"""
    parser = argparse.ArgumentParser(description="HTTP MCP UJI Academic Server")
    parser.add_argument("--host", default="0.0.0.0", help="Host to bind to (default: 0.0.0.0)")
    parser.add_argument("--port", type=int, default=8084, help="Port to bind to (default: 8084)")
    parser.add_argument("--reload", action="store_true", help="Enable auto-reload for development")
    
    args = parser.parse_args()
    
    logger.info(f"Starting HTTP MCP UJI Academic Server on {args.host}:{args.port}")
    
    uvicorn.run(
        "remote_server:app",
        host=args.host,
        port=args.port,
        reload=args.reload,
        log_level="info"
    )


if __name__ == "__main__":
    main()