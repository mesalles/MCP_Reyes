# %% MCP UJI Academic Server
## Main MCP server implementation for UJI Academic Information System

import asyncio
import json
import logging
from typing import Any, Dict, List, Optional, Union
from contextlib import asynccontextmanager

# MCP imports
from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import (
    Resource, Tool, TextContent, ImageContent, EmbeddedResource,
    LoggingLevel
)

# Local imports
from api_client import UJIAcademicClient, create_uji_client
from models import (
    Subject, Degree, Location, ScheduleEvent, APIError,
    SubjectsResponse, DegreesResponse, LocationsResponse, ScheduleResponse
)

# Import exception for proper exception handling
import requests

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# %% Constants
## Constants for repeated strings and configuration

SUBJECT_ID_DESC = "Subject identifier (e.g., 'AE1003')"
DEGREE_ID_DESC = "Degree program identifier (e.g., '208')"
LANGUAGE_ENUM = ["ca", "es", "en"]

# %% Server Configuration
## MCP server configuration and initialization

class MCPUJIServer:
    """MCP server for UJI Academic Information System"""
    
    def __init__(self):
        self.server = Server("mcp-uji-academic")
        self.client: Optional[UJIAcademicClient] = None
        self.setup_tools()
        self.setup_resources()
    
    def setup_tools(self):
        """Setup all MCP tools for the server"""
        
        # %% Subject Management Tools
        ## Tools for managing subjects (asignaturas)
        
        @self.server.list_tools()
        async def handle_list_tools() -> List[Tool]:
            """List all available tools"""
            return [
                Tool(
                    name="get_subjects",
                    description="Get list of subjects with pagination support. Returns subjects from UJI academic system.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "start": {
                                "type": "integer",
                                "description": "Starting record number (default: 0)",
                                "default": 0
                            },
                            "limit": {
                                "type": "integer", 
                                "description": "Number of records to return (default: 20, max: 100)",
                                "default": 20,
                                "maximum": 100
                            },
                            "full": {
                                "type": "boolean",
                                "description": "Return full subject details (default: false)",
                                "default": False
                            }
                        }
                    }
                ),
                Tool(
                    name="get_subject_details",
                    description="Get detailed information for a specific subject by ID",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "subject_id": {
                                "type": "string",
                                "description": SUBJECT_ID_DESC
                            }
                        },
                        "required": ["subject_id"]
                    }
                ),
                Tool(
                    name="get_subject_groups",
                    description="Get groups for a specific subject",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "subject_id": {
                                "type": "string",
                                "description": SUBJECT_ID_DESC
                            }
                        },
                        "required": ["subject_id"]
                    }
                ),
                Tool(
                    name="get_subject_subgroups",
                    description="Get subgroups for a specific subject (includes Theory and Practice groups)",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "subject_id": {
                                "type": "string",
                                "description": SUBJECT_ID_DESC
                            }
                        },
                        "required": ["subject_id"]
                    }
                ),
                Tool(
                    name="search_subjects",
                    description="Search subjects by name or ID with language preference",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "Search query (subject name or ID)"
                            },
                            "language": {
                                "type": "string",
                                "description": "Language preference (ca, es, en)",
                                "enum": ["ca", "es", "en"],
                                "default": "es"
                            }
                        },
                        "required": ["query"]
                    }
                ),
                
                # %% Degree Management Tools
                ## Tools for managing degree programs
                
                Tool(
                    name="get_degrees",
                    description="Get list of all degree programs from UJI",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "full": {
                                "type": "boolean",
                                "description": "Return full degree details (default: true)",
                                "default": True
                            }
                        }
                    }
                ),
                Tool(
                    name="get_degree_details",
                    description="Get detailed information for a specific degree program",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "degree_id": {
                                "type": "string",
                                "description": DEGREE_ID_DESC
                            }
                        },
                        "required": ["degree_id"]
                    }
                ),
                Tool(
                    name="search_degrees",
                    description="Search degree programs by name with language preference",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "Search query (degree name)"
                            },
                            "language": {
                                "type": "string",
                                "description": "Language preference (ca, es, en)",
                                "enum": ["ca", "es", "en"],
                                "default": "es"
                            }
                        },
                        "required": ["query"]
                    }
                ),
                
                # %% Schedule Management Tools
                ## Tools for managing class and exam schedules
                
                Tool(
                    name="get_class_schedule",
                    description="Get class schedule for a degree program in a specific year",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "year": {
                                "type": "string",
                                "description": "Academic year (e.g., '2025')"
                            },
                            "degree_id": {
                                "type": "string",
                                "description": DEGREE_ID_DESC
                            }
                        },
                        "required": ["year", "degree_id"]
                    }
                ),
                Tool(
                    name="get_exam_schedule",
                    description="Get exam schedule for a degree program in a specific year",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "year": {
                                "type": "string",
                                "description": "Academic year (e.g., '2025')"
                            },
                            "degree_id": {
                                "type": "string",
                                "description": DEGREE_ID_DESC
                            }
                        },
                        "required": ["year", "degree_id"]
                    }
                ),
                
                # %% Location Management Tools
                ## Tools for managing university locations
                
                Tool(
                    name="get_locations",
                    description="Get list of all university locations (buildings, classrooms, labs)",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "full": {
                                "type": "boolean",
                                "description": "Return full location details (default: true)",
                                "default": True
                            }
                        }
                    }
                ),
                Tool(
                    name="get_location_details",
                    description="Get detailed information for a specific location",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "location_id": {
                                "type": "string",
                                "description": "Location identifier (e.g., 'ITC156DL')"
                            }
                        },
                        "required": ["location_id"]
                    }
                ),
                Tool(
                    name="search_locations",
                    description="Search university locations by building name or description",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "Search query (building name or location description)"
                            }
                        },
                        "required": ["query"]
                    }
                ),
                
                # %% Utility Tools
                ## Utility and management tools
                
                Tool(
                    name="clear_cache",
                    description="Clear the API client cache to force fresh data retrieval",
                    inputSchema={
                        "type": "object",
                        "properties": {}
                    }
                )
            ]
        
        @self.server.call_tool()
        async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
            """Handle tool calls"""
            
            if not self.client:
                self.client = create_uji_client()
            
            try:
                # %% Subject Tools Implementation
                ## Implementation of subject-related tools
                
                if name == "get_subjects":
                    start = arguments.get("start", 0)
                    limit = min(arguments.get("limit", 20), 100)  # Cap at 100
                    full = arguments.get("full", False)
                    
                    response = self.client.get_subjects(start=start, limit=limit, full=full)
                    
                    return [TextContent(
                        type="text",
                        text=json.dumps({
                            "subjects": [subject.model_dump() for subject in response.content],
                            "pagination": response.page.model_dump() if response.page else None,
                            "total_subjects": len(response.content)
                        }, indent=2, ensure_ascii=False)
                    )]
                
                elif name == "get_subject_details":
                    subject_id = arguments["subject_id"]
                    subject = self.client.get_subject_details(subject_id)
                    
                    return [TextContent(
                        type="text",
                        text=json.dumps(subject.model_dump(), indent=2, ensure_ascii=False)
                    )]
                
                elif name == "get_subject_groups":
                    subject_id = arguments["subject_id"]
                    response = self.client.get_subject_groups(subject_id)
                    
                    return [TextContent(
                        type="text",
                        text=json.dumps({
                            "subject_id": subject_id,
                            "groups": [group.model_dump() for group in response.content],
                            "total_groups": len(response.content)
                        }, indent=2, ensure_ascii=False)
                    )]
                
                elif name == "get_subject_subgroups":
                    subject_id = arguments["subject_id"]
                    response = self.client.get_subject_subgroups(subject_id)
                    
                    # Categorize subgroups by type
                    theory_groups = [sg for sg in response.content if sg.tipo == "TE"]
                    practice_groups = [sg for sg in response.content if sg.tipo == "PR"]
                    other_groups = [sg for sg in response.content if sg.tipo not in ["TE", "PR"]]
                    
                    return [TextContent(
                        type="text",
                        text=json.dumps({
                            "subject_id": subject_id,
                            "subgroups": {
                                "theory": [sg.model_dump() for sg in theory_groups],
                                "practice": [sg.model_dump() for sg in practice_groups],
                                "other": [sg.model_dump() for sg in other_groups]
                            },
                            "total_subgroups": len(response.content)
                        }, indent=2, ensure_ascii=False)
                    )]
                
                elif name == "search_subjects":
                    query = arguments["query"]
                    language = arguments.get("language", "es")
                    
                    subjects = self.client.search_subjects(query, language)
                    
                    return [TextContent(
                        type="text",
                        text=json.dumps({
                            "query": query,
                            "language": language,
                            "results": [subject.model_dump() for subject in subjects],
                            "total_results": len(subjects)
                        }, indent=2, ensure_ascii=False)
                    )]
                
                # %% Degree Tools Implementation
                ## Implementation of degree-related tools
                
                elif name == "get_degrees":
                    full = arguments.get("full", True)
                    response = self.client.get_degrees(full=full)
                    
                    return [TextContent(
                        type="text",
                        text=json.dumps({
                            "degrees": [degree.model_dump() for degree in response.content],
                            "total_degrees": len(response.content)
                        }, indent=2, ensure_ascii=False)
                    )]
                
                elif name == "get_degree_details":
                    degree_id = arguments["degree_id"]
                    degree = self.client.get_degree_details(degree_id)
                    
                    return [TextContent(
                        type="text",
                        text=json.dumps(degree.model_dump(), indent=2, ensure_ascii=False)
                    )]
                
                elif name == "search_degrees":
                    query = arguments["query"]
                    language = arguments.get("language", "es")
                    
                    degrees = self.client.search_degrees(query, language)
                    
                    return [TextContent(
                        type="text",
                        text=json.dumps({
                            "query": query,
                            "language": language,
                            "results": [degree.model_dump() for degree in degrees],
                            "total_results": len(degrees)
                        }, indent=2, ensure_ascii=False)
                    )]
                
                # %% Schedule Tools Implementation
                ## Implementation of schedule-related tools
                
                elif name == "get_class_schedule":
                    year = arguments["year"]
                    degree_id = arguments["degree_id"]
                    
                    response = self.client.get_class_schedule(year, degree_id)
                    
                    return [TextContent(
                        type="text",
                        text=json.dumps({
                            "year": year,
                            "degree_id": degree_id,
                            "schedule": response.model_dump(),
                            "summary": {
                                "total_events": response.total_events,
                                "date_range": response.date_range
                            }
                        }, indent=2, ensure_ascii=False, default=str)
                    )]
                
                elif name == "get_exam_schedule":
                    year = arguments["year"]
                    degree_id = arguments["degree_id"]
                    
                    response = self.client.get_exam_schedule(year, degree_id)
                    
                    return [TextContent(
                        type="text",
                        text=json.dumps({
                            "year": year,
                            "degree_id": degree_id,
                            "exam_schedule": response.model_dump(),
                            "summary": {
                                "total_exams": response.total_events,
                                "date_range": response.date_range
                            }
                        }, indent=2, ensure_ascii=False, default=str)
                    )]
                
                # %% Location Tools Implementation
                ## Implementation of location-related tools
                
                elif name == "get_locations":
                    full = arguments.get("full", True)
                    response = self.client.get_locations(full=full)
                    
                    return [TextContent(
                        type="text",
                        text=json.dumps({
                            "locations": [location.model_dump() for location in response.content],
                            "total_locations": len(response.content)
                        }, indent=2, ensure_ascii=False)
                    )]
                
                elif name == "get_location_details":
                    location_id = arguments["location_id"]
                    location = self.client.get_location_details(location_id)
                    
                    return [TextContent(
                        type="text",
                        text=json.dumps(location.model_dump(), indent=2, ensure_ascii=False)
                    )]
                
                elif name == "search_locations":
                    query = arguments["query"]
                    locations = self.client.search_locations(query)
                    
                    return [TextContent(
                        type="text",
                        text=json.dumps({
                            "query": query,
                            "results": [location.model_dump() for location in locations],
                            "total_results": len(locations)
                        }, indent=2, ensure_ascii=False)
                    )]
                
                # %% Utility Tools Implementation
                ## Implementation of utility tools
                
                elif name == "clear_cache":
                    self.client.clear_cache()
                    return [TextContent(
                        type="text",
                        text=json.dumps({
                            "message": "API client cache cleared successfully",
                            "timestamp": str(asyncio.get_event_loop().time())
                        }, indent=2)
                    )]
                
                else:
                    return [TextContent(
                        type="text",
                        text=json.dumps({
                            "error": "Unknown tool",
                            "tool_name": name,
                            "available_tools": [
                                "get_subjects", "get_subject_details", "get_subject_groups", 
                                "get_subject_subgroups", "search_subjects",
                                "get_degrees", "get_degree_details", "search_degrees",
                                "get_class_schedule", "get_exam_schedule",
                                "get_locations", "get_location_details", "search_locations",
                                "clear_cache"
                            ]
                        }, indent=2)
                    )]
            
            except Exception as api_error:
                # Handle API errors (from our APIError model or other exceptions)
                if hasattr(api_error, 'error') and hasattr(api_error, 'message'):
                    logger.error(f"API error in tool {name}: {api_error}")
                    return [TextContent(
                        type="text",
                        text=json.dumps({
                            "error": getattr(api_error, 'error', 'API_ERROR'),
                            "message": getattr(api_error, 'message', str(api_error)),
                            "status_code": getattr(api_error, 'status_code', 0),
                            "endpoint": getattr(api_error, 'endpoint', None),
                            "tool": name
                        }, indent=2)
                    )]
                else:
                    # Handle other exceptions
                    logger.error(f"Unexpected error in tool {name}: {api_error}")
                    return [TextContent(
                        type="text",
                        text=json.dumps({
                            "error": "INTERNAL_ERROR",
                            "message": str(api_error),
                            "tool": name
                        }, indent=2)
                    )]
    
    def setup_resources(self):
        """Setup MCP resources"""
        
        @self.server.list_resources()
        async def handle_list_resources() -> List[Resource]:
            """List available resources"""
            return [
                Resource(
                    uri="uji://api/info",
                    name="UJI Academic API Information",
                    description="Information about UJI Academic API endpoints and usage",
                    mimeType="application/json"
                )
            ]
        
        @self.server.read_resource()
        async def handle_read_resource(uri: str) -> str:
            """Read resource content"""
            if uri == "uji://api/info":
                return json.dumps({
                    "name": "UJI Academic Information System API",
                    "description": "Access to Universitat Jaume I academic data",
                    "version": "1.0.0",
                    "endpoints": {
                        "subjects": {
                            "base_url": "http://ujiapps.uji.es/lod-autorest/api/datasets/asignaturas",
                            "description": "Subject information and management"
                        },
                        "degrees": {
                            "base_url": "http://ujiapps.uji.es/lod-autorest/api/datasets/estudios",
                            "description": "Degree program information"
                        },
                        "schedules": {
                            "base_url": "http://ujiapps.uji.es/sia/rest/publicacion/",
                            "description": "Class and exam schedules in iCalendar format"
                        },
                        "locations": {
                            "base_url": "http://ujiapps.uji.es/lod-autorest/api/datasets/ubicaciones",
                            "description": "University location information"
                        }
                    },
                    "features": [
                        "Multilingual support (Catalan, Spanish, English)",
                        "Pagination support",
                        "Search functionality",
                        "Calendar parsing",
                        "Caching for performance"
                    ]
                }, indent=2)
            else:
                raise ValueError(f"Unknown resource: {uri}")

    # %% Server Lifecycle
    ## Server startup and shutdown methods
    
    def cleanup(self):
        """Cleanup resources"""
        if self.client:
            self.client.close()
            logger.info("API client closed")


# %% Server Entry Point
## Main entry point for running the MCP server

async def main():
    """Main entry point for the MCP server"""
    logger.info("Starting MCP UJI Academic Server...")
    
    # Create server instance
    mcp_server = MCPUJIServer()
    
    try:
        # Setup cleanup on server shutdown
        async with stdio_server() as streams:
            logger.info("Server running with stdio transport")
            await mcp_server.server.run(
                streams[0], streams[1],
                InitializationOptions(
                    server_name="mcp-uji-academic",
                    server_version="1.0.0",
                    capabilities=mcp_server.server.get_capabilities()
                )
            )
    except KeyboardInterrupt:
        logger.info("Server interrupted by user")
    except Exception as e:
        logger.error(f"Server error: {e}")
        raise
    finally:
        mcp_server.cleanup()
        logger.info("MCP UJI Academic Server stopped")


if __name__ == "__main__":
    asyncio.run(main())