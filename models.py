# %% Data Models
## Pydantic models for Reyes API responses

from typing import Optional, List, Any, Dict
from pydantic import BaseModel, Field
from datetime import datetime


# %% Base Response Models
## Common structures used across different API endpoints

class PageInfo(BaseModel):
    """Pagination information for API responses"""
    rowCount: int = Field(description="Total number of records available")
    pageSize: Optional[int] = Field(default=None, description="Number of records per page")
    startRecord: int = Field(default=0, description="Starting record number for current page")


class Link(BaseModel):
    """Link information for pagination navigation"""
    rel: str = Field(description="Relationship type (e.g., 'next', 'prev')")
    href: str = Field(description="URL for the linked resource")


class BaseResponse(BaseModel):
    """Base response structure for paginated API endpoints"""
    links: Optional[List[Link]] = Field(default_factory=list, description="Navigation links")
    page: Optional[PageInfo] = Field(description="Pagination information")


# %% domain-tools Models
## Models for domain-tools related API responses

# class Domain(BaseModel):
#     """Individual domain information"""
#     success: bool = Field(description="Indicates if the response is valid")
#     data: Dict[str, Any] = Field(description="Information about the domain")
#     error: Optional[List[Optional[str]]] = Field(default=None)

class DomainResponse(BaseModel):
    """Response for domain-tools endpoint"""
    success: bool = Field(description="Indicates if the response is valid")
    data: Dict[str, Any] = Field(description="Information about the domain")
    error: Optional[List[Optional[str]]] = Field(default=None)

class VirustotalResponse(BaseModel):
    """Response for virustotal endpoint"""
    success: bool = Field(description="Indicates if the response is valid")
    data: Dict[str, Any] = Field(description="Information about the ip address")
    error: Optional[List[Optional[str]]] = Field(default=None)

class CriminalIPResponse(BaseModel):
    """Response for criminalIP endpoint"""
    success: bool = Field(description="Indicates if the response is valid")
    data: Dict[str, Any] = Field(description="Information about the ip address")
    error: Optional[List[Optional[str]]] = Field(default=None)

# class Subject(BaseModel):
#     """Individual subject information"""
#     id: str = Field(alias="_id", description="Unique subject identifier (e.g., 'AE1001')")
#     nombreCA: Optional[str] = Field(default=None, description="Subject name in Catalan")
#     nombreES: Optional[str] = Field(default=None, description="Subject name in Spanish") 
#     nombreEN: Optional[str] = Field(default=None, description="Subject name in English")
#     estudiantesMatriculados: Optional[str] = Field(default=None, description="Number of enrolled students")
#     creditos: Optional[str] = Field(default=None, description="ECTS credits")
#     curso: Optional[str] = Field(default=None, description="Academic year/level")
#     semestre: Optional[str] = Field(default=None, description="Semester (1 or 2)")
#     tipo: Optional[str] = Field(default=None, description="Subject type")
#     departamento: Optional[str] = Field(default=None, description="Department")

# class SubjectsResponse(BaseResponse):
#     """Response for subjects list endpoint"""
#     content: List[Subject] = Field(description="List of subjects")

# class SubjectGroup(BaseModel):
#     """Subject group information"""
#     id: str = Field(alias="_id", description="Group identifier")
#     nombre: Optional[str] = Field(default=None, description="Group name")
#     tipo: Optional[str] = Field(default=None, description="Group type")
#     plazas: Optional[str] = Field(default=None, description="Available places")
#     ocupadas: Optional[str] = Field(default=None, description="Occupied places")

# class SubjectGroupsResponse(BaseResponse):
#     """Response for subject groups endpoint"""
#     content: List[SubjectGroup] = Field(description="List of subject groups")

# class SubjectSubgroup(BaseModel):
#     """Subject subgroup information"""
#     id: str = Field(alias="_id", description="Subgroup identifier")
#     nombre: Optional[str] = Field(default=None, description="Subgroup name")
#     tipo: Optional[str] = Field(default=None, description="Subgroup type (TE=Theory, PR=Practice)")
#     grupo: Optional[str] = Field(default=None, description="Parent group")
#     profesor: Optional[str] = Field(default=None, description="Professor name")
#     horario: Optional[str] = Field(default=None, description="Schedule information")

# class SubjectSubgroupsResponse(BaseResponse):
#     """Response for subject subgroups endpoint"""
#     content: List[SubjectSubgroup] = Field(description="List of subject subgroups")

# %% Degree Models
## Models for degree program (estudios) related API responses

# class Degree(BaseModel):
#     """Individual degree program information"""
#     id: str = Field(alias="_id", description="Unique degree identifier")
#     estudioNombreEN: Optional[str] = Field(default=None, description="Degree name in English")
#     estudioNombreCA: Optional[str] = Field(default=None, description="Degree name in Catalan")
#     estudioNombreES: Optional[str] = Field(default=None, description="Degree name in Spanish")
#     tipoDescripcionCA: Optional[str] = Field(default=None, description="Degree type in Catalan")
#     tipoDescripcionES: Optional[str] = Field(default=None, description="Degree type in Spanish")
#     tipo: Optional[str] = Field(default=None, description="Degree type code (G=Grado, M=Master, etc.)")
#     centro: Optional[str] = Field(default=None, description="Faculty/School")
#     creditos: Optional[str] = Field(default=None, description="Total ECTS credits")
#     duracion: Optional[str] = Field(default=None, description="Duration in years")


# class DegreesResponse(BaseResponse):
#     """Response for degrees list endpoint"""
#     content: List[Degree] = Field(description="List of degree programs")


# %% Location Models
## Models for location (ubicaciones) related API responses

# class Location(BaseModel):
#     """Individual location information"""
#     id: str = Field(alias="_id", description="Unique location identifier")
#     edificio: Optional[str] = Field(default=None, description="Building name")
#     descripcion: Optional[str] = Field(default=None, description="Location description/room number")
#     metros: Optional[str] = Field(default=None, description="Area in square meters")
#     planta: Optional[str] = Field(default=None, description="Floor number")
#     capacidad: Optional[str] = Field(default=None, description="Capacity/number of seats")
#     tipo: Optional[str] = Field(default=None, description="Location type (classroom, lab, etc.)")


# class LocationsResponse(BaseResponse):
#     """Response for locations list endpoint"""
#     content: List[Location] = Field(description="List of locations")


# %% Schedule Models
## Models for schedule-related data (iCalendar parsing)

# class ScheduleEvent(BaseModel):
#     """Individual schedule event from iCalendar data"""
#     uid: str = Field(description="Unique event identifier")
#     summary: Optional[str] = Field(default=None, description="Event summary/title")
#     description: Optional[str] = Field(default=None, description="Event description")
#     location: Optional[str] = Field(default=None, description="Event location")
#     start_time: Optional[datetime] = Field(description="Event start time")
#     end_time: Optional[datetime] = Field(description="Event end time")
#     subject_id: Optional[str] = Field(default=None, description="Related subject identifier")
#     group: Optional[str] = Field(default=None, description="Group information")
#     professor: Optional[str] = Field(default=None, description="Professor name")
#     event_type: Optional[str] = Field(default=None, description="Event type (class, exam, etc.)")


# class ScheduleResponse(BaseModel):
#     """Response for schedule endpoints"""
#     events: List[ScheduleEvent] = Field(description="List of schedule events")
#     total_events: int = Field(description="Total number of events")
#     date_range: Optional[Dict[str, str]] = Field(description="Date range of events")


# %% Error Models
## Models for error handling

class APIError(BaseModel):
    """API error information"""
    error: str = Field(description="Error type")
    message: str = Field(description="Error message")
    status_code: int = Field(description="HTTP status code")
    endpoint: Optional[str] = Field(default=None, description="API endpoint that caused the error")


# %% Search and Filter Models
## Models for search and filtering functionality

class SearchParams(BaseModel):
    """Parameters for search operations"""
    query: Optional[str] = Field(default=None, description="Search query string")
    language: Optional[str] = Field(default=None, description="Language preference (ca, es, en)")
    degree_id: Optional[str] = Field(default=None, description="Filter by degree program")
    semester: Optional[str] = Field(default=None, description="Filter by semester")
    course: Optional[str] = Field(default=None, description="Filter by course/year")
    subject_type: Optional[str] = Field(default=None, description="Filter by subject type")


class PaginationParams(BaseModel):
    """Parameters for pagination"""
    start: int = Field(default=0, description="Starting record number")
    limit: int = Field(default=20, description="Number of records to return")
    full: bool = Field(default=False, description="Return full details")