# %% Reyes API Client
## Client for interacting with Reyes APIs

import asyncio
import logging
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
import requests
import aiohttp
from icalendar import Calendar, Event
from models import (
    Subject, SubjectsResponse, APIError, PaginationParams
)
# from models import (
#     Subject, SubjectsResponse, SubjectGroupsResponse, SubjectSubgroupsResponse,
#     Degree, DegreesResponse, Location, LocationsResponse,
#     ScheduleEvent, ScheduleResponse, APIError, PaginationParams
# )

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# %% Configuration
## Base URLs and configuration settings

class ReyesConfig:
    """Configuration settings for Reyes API client"""
    
    # Base URLs for different API endpoints
    TOOLS_API_BASE = "https://reyes.ccn-cert.cni.es/apireyes/api/v4/search/tool/"
    
    # Default values
    DEFAULT_TIMEOUT = 30
    DEFAULT_PAGE_SIZE = 20
    CACHE_EXPIRY_MINUTES = 15
    
    # Headers
    CALENDAR_HEADERS = {"Content-Type": "text/calendar"}
    JSON_HEADERS = {"Content-Type": "application/json"}

# class UJIConfig:
#     """Configuration settings for UJI API client"""
    
#     # Base URLs for different API endpoints
#     ACADEMIC_API_BASE = "http://ujiapps.uji.es/lod-autorest/api/datasets/"
#     SCHEDULE_API_BASE = "http://ujiapps.uji.es/sia/rest/publicacion/"
    
#     # Default values
#     DEFAULT_TIMEOUT = 30
#     DEFAULT_PAGE_SIZE = 20
#     CACHE_EXPIRY_MINUTES = 15
    
#     # Headers
#     CALENDAR_HEADERS = {"Content-Type": "text/calendar"}
#     JSON_HEADERS = {"Content-Type": "application/json"}


# %% Cache Implementation
## Simple in-memory cache with expiration

class SimpleCache:
    """Simple in-memory cache with expiration"""
    
    def __init__(self):
        self._cache: Dict[str, Dict[str, Any]] = {}
    
    def get(self, key: str) -> Optional[Any]:
        """Get cached value if not expired"""
        if key in self._cache:
            entry = self._cache[key]
            if datetime.now() < entry["expires"]:
                logger.debug(f"Cache hit for key: {key}")
                return entry["value"]
            else:
                del self._cache[key]
                logger.debug(f"Cache expired for key: {key}")
        return None
    
    def set(self, key: str, value: Any, expiry_minutes: int = ReyesConfig.CACHE_EXPIRY_MINUTES):
        """Set cached value with expiration"""
        self._cache[key] = {
            "value": value,
            "expires": datetime.now() + timedelta(minutes=expiry_minutes)
        }
        logger.debug(f"Cached value for key: {key}")
    
    def clear(self):
        """Clear all cached values"""
        self._cache.clear()
        logger.debug("Cache cleared")


# %% Reyes API Client
## Main client class for Reyes APIs

class ReyesClient:
    """Client for Reyes APIs"""
    
    def __init__(self, timeout: int = ReyesConfig.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.cache = SimpleCache()
        self.session = requests.Session()
        self.session.timeout = timeout
    
    def _make_request(self, url: str, headers: Optional[Dict[str, str]] = None, 
                     params: Optional[Dict[str, Any]] = None, use_cache: bool = True) -> Any:
        """Make HTTP request with error handling and caching"""
        cache_key = f"{url}_{str(params)}_{str(headers)}"
        
        # Check cache first
        if use_cache:
            cached_result = self.cache.get(cache_key)
            if cached_result is not None:
                return cached_result
        
        try:
            logger.info(f"Making request to: {url}")
            response = self.session.get(url, headers=headers, params=params)
            response.raise_for_status()
            
            # Determine response type and parse accordingly
            content_type = response.headers.get('content-type', '').lower()
            
            if 'application/json' in content_type:
                result = response.json()
            elif 'text/calendar' in content_type or 'text/plain' in content_type:
                result = response.text
            else:
                result = response.text
            
            # Cache successful responses
            if use_cache and response.status_code == 200:
                self.cache.set(cache_key, result)
            
            return result
            
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error for {url}: {e}")
            raise APIError(
                error="HTTP_ERROR",
                message=f"HTTP {e.response.status_code}: {str(e)}",
                status_code=e.response.status_code,
                endpoint=url
            )
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error for {url}: {e}")
            raise APIError(
                error="REQUEST_ERROR",
                message=str(e),
                status_code=0,
                endpoint=url
            )
        except Exception as e:
            logger.error(f"Unexpected error for {url}: {e}")
            raise APIError(
                error="UNKNOWN_ERROR",
                message=str(e),
                status_code=0,
                endpoint=url
            )

# %% UJI API Client
## Main client class for UJI Academic APIs

# class UJIAcademicClient:
#     """Client for UJI Academic Information System APIs"""
    
#     def __init__(self, timeout: int = ReyesConfig.DEFAULT_TIMEOUT):
#         self.timeout = timeout
#         self.cache = SimpleCache()
#         self.session = requests.Session()
#         self.session.timeout = timeout
    
#     def _make_request(self, url: str, headers: Optional[Dict[str, str]] = None, 
#                      params: Optional[Dict[str, Any]] = None, use_cache: bool = True) -> Any:
#         """Make HTTP request with error handling and caching"""
#         cache_key = f"{url}_{str(params)}_{str(headers)}"
        
#         # Check cache first
#         if use_cache:
#             cached_result = self.cache.get(cache_key)
#             if cached_result is not None:
#                 return cached_result
        
#         try:
#             logger.info(f"Making request to: {url}")
#             response = self.session.get(url, headers=headers, params=params)
#             response.raise_for_status()
            
#             # Determine response type and parse accordingly
#             content_type = response.headers.get('content-type', '').lower()
            
#             if 'application/json' in content_type:
#                 result = response.json()
#             elif 'text/calendar' in content_type or 'text/plain' in content_type:
#                 result = response.text
#             else:
#                 result = response.text
            
#             # Cache successful responses
#             if use_cache and response.status_code == 200:
#                 self.cache.set(cache_key, result)
            
#             return result
            
#         except requests.exceptions.HTTPError as e:
#             logger.error(f"HTTP error for {url}: {e}")
#             raise APIError(
#                 error="HTTP_ERROR",
#                 message=f"HTTP {e.response.status_code}: {str(e)}",
#                 status_code=e.response.status_code,
#                 endpoint=url
#             )
#         except requests.exceptions.RequestException as e:
#             logger.error(f"Request error for {url}: {e}")
#             raise APIError(
#                 error="REQUEST_ERROR",
#                 message=str(e),
#                 status_code=0,
#                 endpoint=url
#             )
#         except Exception as e:
#             logger.error(f"Unexpected error for {url}: {e}")
#             raise APIError(
#                 error="UNKNOWN_ERROR",
#                 message=str(e),
#                 status_code=0,
#                 endpoint=url
#             )

    # %% Tools Methods
    ## Methods for tools-related API endpoints
    
    def domaintools(self, query: str ="",) -> SubjectsResponse:
        """Query domain-tools tool"""
        url = f"{ReyesConfig.TOOLS_API_BASE}domain-tools"
        params = {"q": query}

        data = self._make_request(url, params=params)
        return SubjectsResponse(**data)
    
    # def get_subjects(self, start: int = 0, limit: int = 20, full: bool = False) -> SubjectsResponse:
    #     """Get list of subjects with pagination"""
    #     url = f"{UJIConfig.ACADEMIC_API_BASE}asignaturas"
    #     params = {"start": start, "limit": limit}
    #     if full:
    #         params["full"] = "true"
        
    #     data = self._make_request(url, params=params)
    #     return SubjectsResponse(**data)
    
    # def get_subject_details(self, subject_id: str) -> Subject:
    #     """Get detailed information for a specific subject"""
    #     url = f"{UJIConfig.ACADEMIC_API_BASE}asignaturas/{subject_id}"
    #     data = self._make_request(url)
    #     return Subject(**data)
    
    # def get_subject_groups(self, subject_id: str) -> SubjectGroupsResponse:
    #     """Get groups for a specific subject"""
    #     url = f"{UJIConfig.ACADEMIC_API_BASE}asignaturas/{subject_id}/grupos"
    #     data = self._make_request(url)
    #     return SubjectGroupsResponse(**data)
    
    # def get_subject_subgroups(self, subject_id: str) -> SubjectSubgroupsResponse:
    #     """Get subgroups for a specific subject"""
    #     url = f"{UJIConfig.ACADEMIC_API_BASE}asignaturas/{subject_id}/grupos/subgrupos"
    #     data = self._make_request(url)
    #     return SubjectSubgroupsResponse(**data)
    
    # def search_subjects(self, query: str, language: str = "es") -> List[Subject]:
    #     """Search subjects by name or ID"""
    #     # Get all subjects and filter by query
    #     subjects_response = self.get_subjects(limit=1000, full=True)
        
    #     query_lower = query.lower()
    #     matching_subjects = []
        
    #     for subject in subjects_response.content:
    #         # Search in ID
    #         if query_lower in subject.id.lower():
    #             matching_subjects.append(subject)
    #             continue
            
    #         # Search in names based on language preference
    #         name_field = f"nombre{language.upper()}"
    #         if hasattr(subject, name_field):
    #             name = getattr(subject, name_field)
    #             if name and query_lower in name.lower():
    #                 matching_subjects.append(subject)
    #                 continue
            
    #         # Fallback to search in all name fields
    #         for name_attr in ["nombreES", "nombreCA", "nombreEN"]:
    #             name = getattr(subject, name_attr)
    #             if name and query_lower in name.lower():
    #                 matching_subjects.append(subject)
    #                 break
        
    #     return matching_subjects

    # %% Degree Methods
    ## Methods for degree program related API endpoints
    
    # def get_degrees(self, full: bool = True) -> DegreesResponse:
    #     """Get list of degree programs"""
    #     url = f"{UJIConfig.ACADEMIC_API_BASE}estudios"
    #     params = {}
    #     if full:
    #         params["full"] = "true"
        
    #     data = self._make_request(url, params=params)
    #     return DegreesResponse(**data)
    
    # def get_degree_details(self, degree_id: str) -> Degree:
    #     """Get detailed information for a specific degree program"""
    #     url = f"{UJIConfig.ACADEMIC_API_BASE}estudios/{degree_id}"
    #     data = self._make_request(url)
    #     return Degree(**data)
    
    # def search_degrees(self, query: str, language: str = "es") -> List[Degree]:
    #     """Search degree programs by name"""
    #     degrees_response = self.get_degrees(full=True)
        
    #     query_lower = query.lower()
    #     matching_degrees = []
        
    #     for degree in degrees_response.content:
    #         # Search in names based on language preference
    #         name_field = f"estudioNombre{language.upper()}"
    #         if hasattr(degree, name_field):
    #             name = getattr(degree, name_field)
    #             if name and query_lower in name.lower():
    #                 matching_degrees.append(degree)
    #                 continue
            
    #         # Fallback to search in all name fields
    #         for name_attr in ["estudioNombreES", "estudioNombreCA", "estudioNombreEN"]:
    #             name = getattr(degree, name_attr)
    #             if name and query_lower in name.lower():
    #                 matching_degrees.append(degree)
    #                 break
        
    #     return matching_degrees

    # # %% Location Methods
    # ## Methods for location related API endpoints
    
    # def get_locations(self, full: bool = True) -> LocationsResponse:
    #     """Get list of university locations"""
    #     url = f"{UJIConfig.ACADEMIC_API_BASE}ubicaciones"
    #     params = {}
    #     if full:
    #         params["full"] = "true"
        
    #     data = self._make_request(url, params=params)
    #     return LocationsResponse(**data)
    
    # def get_location_details(self, location_id: str) -> Location:
    #     """Get detailed information for a specific location"""
    #     url = f"{UJIConfig.ACADEMIC_API_BASE}ubicaciones/{location_id}"
    #     data = self._make_request(url)
    #     return Location(**data)
    
    # def search_locations(self, query: str) -> List[Location]:
    #     """Search locations by building name or description"""
    #     locations_response = self.get_locations(full=True)
        
    #     query_lower = query.lower()
    #     matching_locations = []
        
    #     for location in locations_response.content:
    #         # Search in building name
    #         if location.edificio and query_lower in location.edificio.lower():
    #             matching_locations.append(location)
    #             continue
            
    #         # Search in description
    #         if location.descripcion and query_lower in location.descripcion.lower():
    #             matching_locations.append(location)
    #             continue
            
    #         # Search in location ID
    #         if query_lower in location.id.lower():
    #             matching_locations.append(location)
        
    #     return matching_locations

    # # %% Schedule Methods
    # ## Methods for schedule related API endpoints
    
    # def _parse_icalendar(self, calendar_text: str) -> List[ScheduleEvent]:
    #     """Parse iCalendar text and extract events"""
    #     events = []
        
    #     try:
    #         cal = Calendar.from_ical(calendar_text)
            
    #         for component in cal.walk():
    #             if component.name == "VEVENT":
    #                 event = ScheduleEvent(
    #                     uid=str(component.get('uid', '')),
    #                     summary=str(component.get('summary', '')),
    #                     description=str(component.get('description', '')),
    #                     location=str(component.get('location', '')),
    #                     start_time=component.get('dtstart').dt if component.get('dtstart') else None,
    #                     end_time=component.get('dtend').dt if component.get('dtend') else None,
    #                 )
                    
    #                 # Extract additional information from description or summary
    #                 summary_text = event.summary or ""
    #                 description_text = event.description or ""
                    
    #                 # Try to extract subject ID, group, professor from the text
    #                 # This may need adjustment based on actual calendar format
    #                 if summary_text:
    #                     parts = summary_text.split()
    #                     if parts:
    #                         # First part might be subject ID
    #                         event.subject_id = parts[0] if parts[0].isalnum() else None
                    
    #                 events.append(event)
                    
    #     except Exception as e:
    #         logger.error(f"Error parsing iCalendar: {e}")
    #         # Return empty list if parsing fails
            
    #     return events
    
    # def get_class_schedule(self, year: str, degree_id: str) -> ScheduleResponse:
    #     """Get class schedule for a degree program in iCalendar format"""
    #     url = f"{UJIConfig.SCHEDULE_API_BASE}{year}/estudio/{degree_id}/horarios"
        
    #     calendar_text = self._make_request(url, headers=UJIConfig.CALENDAR_HEADERS)
    #     events = self._parse_icalendar(calendar_text)
        
    #     # Calculate date range
    #     date_range = None
    #     if events:
    #         start_dates = [e.start_time for e in events if e.start_time]
    #         end_dates = [e.end_time for e in events if e.end_time]
            
    #         if start_dates and end_dates:
    #             date_range = {
    #                 "start": min(start_dates).isoformat() if start_dates else None,
    #                 "end": max(end_dates).isoformat() if end_dates else None
    #             }
        
    #     return ScheduleResponse(
    #         events=events,
    #         total_events=len(events),
    #         date_range=date_range
    #     )
    
    # def get_exam_schedule(self, year: str, degree_id: str) -> ScheduleResponse:
    #     """Get exam schedule for a degree program in iCalendar format"""
    #     url = f"{UJIConfig.SCHEDULE_API_BASE}{year}/estudio/{degree_id}/examenes"
        
    #     calendar_text = self._make_request(url, headers=UJIConfig.CALENDAR_HEADERS)
    #     events = self._parse_icalendar(calendar_text)
        
    #     # Mark all events as exam type
    #     for event in events:
    #         event.event_type = "exam"
        
    #     # Calculate date range
    #     date_range = None
    #     if events:
    #         start_dates = [e.start_time for e in events if e.start_time]
    #         end_dates = [e.end_time for e in events if e.end_time]
            
    #         if start_dates and end_dates:
    #             date_range = {
    #                 "start": min(start_dates).isoformat() if start_dates else None,
    #                 "end": max(end_dates).isoformat() if end_dates else None
    #             }
        
    #     return ScheduleResponse(
    #         events=events,
    #         total_events=len(events),
    #         date_range=date_range
    #     )

    # %% Utility Methods
    ## Helper methods for client functionality
    
    def clear_cache(self):
        """Clear the internal cache"""
        self.cache.clear()
        logger.info("API client cache cleared")
    
    def close(self):
        """Close the HTTP session"""
        self.session.close()
        logger.info("API client session closed")
    
    def __enter__(self):
        """Context manager entry"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()


# %% Factory Function
## Factory function for creating client instances

def create_uji_client(timeout: int = ReyesConfig.DEFAULT_TIMEOUT) -> ReyesClient:
    """Factory function to create UJI Academic API client"""
    return ReyesClient(timeout=timeout)