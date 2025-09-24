# MCP UJI Academic Server

A comprehensive Model Context Protocol (MCP) server that provides access to the Universitat Jaume I (UJI) academic information system through REST API endpoints. This server enables seamless integration with UJI's academic data including subjects, degree programs, schedules, and university locations.

## Features

- **Comprehensive Academic Data Access**: Retrieve subjects, degree programs, schedules, and locations
- **Multilingual Support**: Content available in Catalan, Spanish, and English
- **Intelligent Caching**: Built-in caching system for improved performance
- **Search Functionality**: Search across subjects, degrees, and locations
- **Schedule Management**: Parse and manage class and exam schedules in iCalendar format
- **Error Handling**: Robust error handling with meaningful error messages
- **Type Safety**: Full type hints and Pydantic models for data validation

## Installation

### Prerequisites

- Python 3.12 or higher
- UV package manager

### Setup

1. **Clone or download the project**:
   ```bash
   git clone <repository-url>
   cd MCP_UJI_academic
   ```

2. **Install dependencies using UV**:
   ```bash
   uv sync
   ```

3. **Activate the virtual environment**:
   ```bash
   source .venv/bin/activate  # On Linux/macOS
   # or
   .venv\Scripts\activate  # On Windows
   ```

## Usage

### Running the MCP Server

```bash
# Using UV
uv run main.py

# Or with Python directly
python main.py
```

### Integration with MCP Clients

Add the server to your MCP client configuration. Example for Claude Desktop:

```json
{
  "mcpServers": {
    "mcp-uji-academic": {
      "command": "uv",
      "args": ["run", "/path/to/MCP_UJI_academic/main.py"],
      "cwd": "/path/to/MCP_UJI_academic"
    }
  }
}
```

## Available Tools

### Subject Management

#### `get_subjects`
Retrieve a paginated list of subjects from the UJI academic system.

**Parameters:**
- `start` (optional): Starting record number (default: 0)
- `limit` (optional): Number of records to return (default: 20, max: 100)
- `full` (optional): Return full subject details (default: false)

**Example:**
```json
{
  "name": "get_subjects",
  "arguments": {
    "start": 0,
    "limit": 10,
    "full": true
  }
}
```

#### `get_subject_details`
Get detailed information for a specific subject.

**Parameters:**
- `subject_id` (required): Subject identifier (e.g., "AE1003")

#### `get_subject_groups`
Get groups for a specific subject.

**Parameters:**
- `subject_id` (required): Subject identifier

#### `get_subject_subgroups`
Get subgroups for a specific subject, including Theory (TE) and Practice (PR) groups.

**Parameters:**
- `subject_id` (required): Subject identifier

#### `search_subjects`
Search subjects by name or ID with language preference.

**Parameters:**
- `query` (required): Search query
- `language` (optional): Language preference ("ca", "es", "en", default: "es")

### Degree Program Management

#### `get_degrees`
Get list of all degree programs.

**Parameters:**
- `full` (optional): Return full degree details (default: true)

#### `get_degree_details`
Get detailed information for a specific degree program.

**Parameters:**
- `degree_id` (required): Degree program identifier (e.g., "208")

#### `search_degrees`
Search degree programs by name.

**Parameters:**
- `query` (required): Search query
- `language` (optional): Language preference ("ca", "es", "en", default: "es")

### Schedule Management

#### `get_class_schedule`
Get class schedule for a degree program in a specific year.

**Parameters:**
- `year` (required): Academic year (e.g., "2025")
- `degree_id` (required): Degree program identifier

#### `get_exam_schedule`
Get exam schedule for a degree program in a specific year.

**Parameters:**
- `year` (required): Academic year (e.g., "2025")
- `degree_id` (required): Degree program identifier

### Location Management

#### `get_locations`
Get list of all university locations.

**Parameters:**
- `full` (optional): Return full location details (default: true)

#### `get_location_details`
Get detailed information for a specific location.

**Parameters:**
- `location_id` (required): Location identifier (e.g., "ITC156DL")

#### `search_locations`
Search university locations by building name or description.

**Parameters:**
- `query` (required): Search query

### Utility Tools

#### `clear_cache`
Clear the API client cache to force fresh data retrieval.

**Parameters:** None

## API Endpoints

The server connects to the following UJI API endpoints:

### Academic Data
- **Base URL**: `http://ujiapps.uji.es/lod-autorest/api/datasets/`
- **Subjects**: `/asignaturas`
- **Degrees**: `/estudios`
- **Locations**: `/ubicaciones`

### Schedule Data
- **Base URL**: `http://ujiapps.uji.es/sia/rest/publicacion/`
- **Class Schedules**: `/{year}/estudio/{degree_id}/horarios`
- **Exam Schedules**: `/{year}/estudio/{degree_id}/examenes`

## Data Models

The server uses Pydantic models for data validation and type safety:

- **Subject**: Subject information with multilingual names
- **Degree**: Degree program details
- **Location**: University location information
- **ScheduleEvent**: Calendar event information
- **API Responses**: Structured responses with pagination

## Example Usage Scenarios

### 1. Finding Subjects for a Degree Program
```json
{
  "name": "search_subjects",
  "arguments": {
    "query": "Mathematics",
    "language": "en"
  }
}
```

### 2. Getting Class Schedule
```json
{
  "name": "get_class_schedule",
  "arguments": {
    "year": "2025",
    "degree_id": "208"
  }
}
```

### 3. Searching University Locations
```json
{
  "name": "search_locations",
  "arguments": {
    "query": "library"
  }
}
```

## Configuration

### Environment Variables

The server supports the following configuration options:

- **API Timeout**: Default 30 seconds
- **Cache Expiry**: Default 15 minutes
- **Page Size**: Default 20 records

### Logging

The server includes comprehensive logging for debugging and monitoring:

```python
import logging
logging.basicConfig(level=logging.INFO)
```

## Error Handling

The server includes robust error handling for:

- HTTP errors (404, 500, etc.)
- Network timeouts
- Malformed JSON responses
- API rate limiting
- Calendar parsing errors

Error responses include:
- Error type and message
- HTTP status code
- Endpoint information
- Tool context

## Performance

### Caching
- In-memory cache with configurable expiration
- Automatic cache invalidation
- Manual cache clearing via `clear_cache` tool

### Optimization
- Connection pooling with requests session
- Efficient pagination handling
- Selective data loading (full vs. summary)

## Development

### Project Structure
```
MCP_UJI_academic/
├── main.py              # Entry point
├── server.py            # MCP server implementation
├── api_client.py        # UJI API client
├── models.py            # Pydantic data models
├── pyproject.toml       # UV project configuration
└── README.md           # Documentation
```

### Dependencies

Core dependencies:
- `mcp>=1.0.0`: Model Context Protocol framework
- `requests>=2.31.0`: HTTP client
- `pydantic>=2.5.0`: Data validation
- `icalendar>=5.0.11`: Calendar parsing
- `aiohttp>=3.9.0`: Async HTTP support
- `python-dateutil>=2.8.0`: Date handling

Development dependencies:
- `pytest>=7.4.0`: Testing framework
- `black>=23.0.0`: Code formatting
- `mypy>=1.5.0`: Type checking
- `ruff>=0.1.0`: Linting

### Running Tests

```bash
# Install development dependencies
uv sync --dev

# Run tests
uv run pytest

# Run with coverage
uv run pytest --cov=. --cov-report=html
```

### Code Quality

```bash
# Format code
uv run black .

# Type checking
uv run mypy .

# Linting
uv run ruff check .
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Run code quality checks
6. Submit a pull request

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Support

For issues and questions:
1. Check the error logs for detailed error messages
2. Verify API endpoint availability
3. Check network connectivity to UJI servers
4. Review the MCP client configuration

## Changelog

### v1.0.0
- Initial release
- Complete UJI Academic API integration
- MCP server implementation
- Multilingual support
- Caching system
- Comprehensive error handling

## Acknowledgments

- Universitat Jaume I for providing the academic data APIs
- Model Context Protocol community for the framework
- Contributors to the open-source dependencies