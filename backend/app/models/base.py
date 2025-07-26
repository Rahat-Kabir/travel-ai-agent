"""
Base models and common utilities.
"""

from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum


class ResponseStatus(str, Enum):
    """Standard response status codes."""
    SUCCESS = "success"
    ERROR = "error"
    PARTIAL = "partial"
    PENDING = "pending"


class BaseResponse(BaseModel):
    """Base response model for all API endpoints."""
    status: ResponseStatus = Field(..., description="Response status")
    message: Optional[str] = Field(None, description="Human-readable message")
    timestamp: datetime = Field(default_factory=datetime.now, description="Response timestamp")
    request_id: Optional[str] = Field(None, description="Unique request identifier")
    
    class Config:
        use_enum_values = True


class ErrorResponse(BaseResponse):
    """Error response model."""
    status: ResponseStatus = ResponseStatus.ERROR
    error_code: Optional[str] = Field(None, description="Machine-readable error code")
    error_details: Optional[Dict[str, Any]] = Field(None, description="Additional error information")


class HealthResponse(BaseModel):
    """Health check response model."""
    status: str = Field(..., description="Service status")
    timestamp: datetime = Field(default_factory=datetime.now)
    version: str = Field(..., description="Service version")
    dependencies: Dict[str, str] = Field(default_factory=dict, description="Dependency status")


class PaginationParams(BaseModel):
    """Pagination parameters."""
    page: int = Field(1, ge=1, description="Page number (1-based)")
    page_size: int = Field(20, ge=1, le=100, description="Items per page")
    
    @property
    def offset(self) -> int:
        """Calculate offset for database queries."""
        return (self.page - 1) * self.page_size


class PaginatedResponse(BaseResponse):
    """Paginated response model."""
    page: int = Field(..., description="Current page number")
    page_size: int = Field(..., description="Items per page")
    total_items: int = Field(..., description="Total number of items")
    total_pages: int = Field(..., description="Total number of pages")
    has_next: bool = Field(..., description="Whether there are more pages")
    has_previous: bool = Field(..., description="Whether there are previous pages")
    
    @classmethod
    def create(
        cls,
        items: list,
        pagination: PaginationParams,
        total_items: int,
        status: ResponseStatus = ResponseStatus.SUCCESS,
        message: Optional[str] = None
    ):
        """Create a paginated response."""
        total_pages = (total_items + pagination.page_size - 1) // pagination.page_size
        
        return cls(
            status=status,
            message=message,
            page=pagination.page,
            page_size=pagination.page_size,
            total_items=total_items,
            total_pages=total_pages,
            has_next=pagination.page < total_pages,
            has_previous=pagination.page > 1,
            data=items
        )


class ValidationError(BaseModel):
    """Validation error details."""
    field: str = Field(..., description="Field that failed validation")
    message: str = Field(..., description="Validation error message")
    value: Optional[Any] = Field(None, description="Invalid value")


class ValidationErrorResponse(ErrorResponse):
    """Validation error response."""
    error_code: str = "VALIDATION_ERROR"
    validation_errors: list[ValidationError] = Field(..., description="List of validation errors")


# Common field validators and utilities
def validate_airport_code(code: str) -> str:
    """Validate airport code format."""
    if not code or len(code) != 3 or not code.isalpha():
        raise ValueError("Airport code must be a 3-letter alphabetic code")
    return code.upper()


def validate_airline_code(code: str) -> str:
    """Validate airline code format."""
    if not code or len(code) != 2 or not code.isalnum():
        raise ValueError("Airline code must be a 2-character alphanumeric code")
    return code.upper()


def validate_date_string(date_str: str) -> str:
    """Validate date string format (YYYY-MM-DD)."""
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return date_str
    except ValueError:
        raise ValueError("Date must be in YYYY-MM-DD format")


# Configuration models
class APIConfig(BaseModel):
    """API configuration settings."""
    title: str = "Travel Agent API"
    description: str = "AI-powered flight search and travel planning API"
    version: str = "1.0.0"
    debug: bool = False
    
    # CORS settings
    cors_origins: list[str] = Field(default_factory=lambda: ["*"])
    cors_methods: list[str] = Field(default_factory=lambda: ["*"])
    cors_headers: list[str] = Field(default_factory=lambda: ["*"])
    
    # Rate limiting
    rate_limit_requests: int = 100
    rate_limit_window: int = 3600  # seconds
    
    # Request/Response settings
    max_request_size: int = 1024 * 1024  # 1MB
    request_timeout: int = 30  # seconds


class DatabaseConfig(BaseModel):
    """Database configuration settings."""
    url: str = Field(..., description="Database connection URL")
    pool_size: int = Field(5, description="Connection pool size")
    max_overflow: int = Field(10, description="Maximum pool overflow")
    pool_timeout: int = Field(30, description="Pool timeout in seconds")
    echo: bool = Field(False, description="Echo SQL queries")


class ExternalAPIConfig(BaseModel):
    """External API configuration."""
    serpapi_key: str = Field(..., description="SerpAPI key")
    serpapi_timeout: int = Field(30, description="SerpAPI request timeout")
    openai_api_key: str = Field(..., description="OpenAI API key")
    openai_model: str = Field("gpt-4o", description="OpenAI model to use")
    openai_temperature: float = Field(0.1, description="OpenAI temperature")
    openai_max_tokens: int = Field(1000, description="OpenAI max tokens")


class LoggingConfig(BaseModel):
    """Logging configuration."""
    level: str = Field("INFO", description="Log level")
    format: str = Field(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        description="Log format"
    )
    file_path: Optional[str] = Field(None, description="Log file path")
    max_file_size: int = Field(10 * 1024 * 1024, description="Max log file size in bytes")
    backup_count: int = Field(5, description="Number of backup log files")
