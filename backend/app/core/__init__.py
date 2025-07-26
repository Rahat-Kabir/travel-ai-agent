"""
Core package for the Travel Agent API.
"""

from .config import Settings, get_settings, load_environment_variables
from .dependencies import (
    get_current_user_id,
    get_api_key,
    validate_api_key,
    get_rate_limit_key,
    check_rate_limit,
    get_request_id,
    get_authenticated_user,
    RateLimiter,
    rate_limiter
)
from .exceptions import (
    TravelAgentException,
    ConfigurationError,
    ExternalAPIError,
    SerpAPIError,
    OpenAIError,
    AgentError,
    FlightSearchError,
    ParameterExtractionError,
    RateLimitError,
    AuthenticationError,
    AuthorizationError,
    ValidationError,
    ConversationError,
    ToolExecutionError,
    get_http_status_code
)

__all__ = [
    "Settings",
    "get_settings",
    "load_environment_variables",
    "get_current_user_id",
    "get_api_key",
    "validate_api_key",
    "get_rate_limit_key",
    "check_rate_limit",
    "get_request_id",
    "get_authenticated_user",
    "RateLimiter",
    "rate_limiter",
    "TravelAgentException",
    "ConfigurationError",
    "ExternalAPIError",
    "SerpAPIError",
    "OpenAIError",
    "AgentError",
    "FlightSearchError",
    "ParameterExtractionError",
    "RateLimitError",
    "AuthenticationError",
    "AuthorizationError",
    "ValidationError",
    "ConversationError",
    "ToolExecutionError",
    "get_http_status_code",
]
