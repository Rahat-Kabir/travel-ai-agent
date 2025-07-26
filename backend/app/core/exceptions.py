"""
Custom exceptions for the Travel Agent API.
"""

from typing import Optional, Dict, Any


class TravelAgentException(Exception):
    """Base exception for Travel Agent API."""
    
    def __init__(
        self,
        message: str,
        error_code: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.error_code = error_code or self.__class__.__name__
        self.details = details or {}
        super().__init__(self.message)


class ConfigurationError(TravelAgentException):
    """Raised when there's a configuration error."""
    pass


class ExternalAPIError(TravelAgentException):
    """Raised when an external API call fails."""
    
    def __init__(
        self,
        message: str,
        api_name: str,
        status_code: Optional[int] = None,
        response_data: Optional[Dict[str, Any]] = None
    ):
        self.api_name = api_name
        self.status_code = status_code
        self.response_data = response_data
        
        details = {
            "api_name": api_name,
            "status_code": status_code,
            "response_data": response_data
        }
        
        super().__init__(message, "EXTERNAL_API_ERROR", details)


class SerpAPIError(ExternalAPIError):
    """Raised when SerpAPI calls fail."""
    
    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        response_data: Optional[Dict[str, Any]] = None
    ):
        super().__init__(message, "SerpAPI", status_code, response_data)


class OpenAIError(ExternalAPIError):
    """Raised when OpenAI API calls fail."""
    
    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        response_data: Optional[Dict[str, Any]] = None
    ):
        super().__init__(message, "OpenAI", status_code, response_data)


class AgentError(TravelAgentException):
    """Raised when the AI agent encounters an error."""
    
    def __init__(
        self,
        message: str,
        agent_state: Optional[Dict[str, Any]] = None,
        retry_count: int = 0
    ):
        self.agent_state = agent_state
        self.retry_count = retry_count
        
        details = {
            "agent_state": agent_state,
            "retry_count": retry_count
        }
        
        super().__init__(message, "AGENT_ERROR", details)


class FlightSearchError(TravelAgentException):
    """Raised when flight search operations fail."""
    
    def __init__(
        self,
        message: str,
        search_params: Optional[Dict[str, Any]] = None,
        validation_errors: Optional[list] = None
    ):
        self.search_params = search_params
        self.validation_errors = validation_errors or []
        
        details = {
            "search_params": search_params,
            "validation_errors": validation_errors
        }
        
        super().__init__(message, "FLIGHT_SEARCH_ERROR", details)


class ParameterExtractionError(TravelAgentException):
    """Raised when parameter extraction from user input fails."""
    
    def __init__(
        self,
        message: str,
        user_input: str,
        missing_params: Optional[list] = None
    ):
        self.user_input = user_input
        self.missing_params = missing_params or []
        
        details = {
            "user_input": user_input,
            "missing_params": missing_params
        }
        
        super().__init__(message, "PARAMETER_EXTRACTION_ERROR", details)


class RateLimitError(TravelAgentException):
    """Raised when rate limits are exceeded."""
    
    def __init__(
        self,
        message: str,
        limit: int,
        window: int,
        retry_after: Optional[int] = None
    ):
        self.limit = limit
        self.window = window
        self.retry_after = retry_after
        
        details = {
            "limit": limit,
            "window": window,
            "retry_after": retry_after
        }
        
        super().__init__(message, "RATE_LIMIT_ERROR", details)


class AuthenticationError(TravelAgentException):
    """Raised when authentication fails."""
    pass


class AuthorizationError(TravelAgentException):
    """Raised when authorization fails."""
    pass


class ValidationError(TravelAgentException):
    """Raised when input validation fails."""
    
    def __init__(
        self,
        message: str,
        field: str,
        value: Any,
        constraint: Optional[str] = None
    ):
        self.field = field
        self.value = value
        self.constraint = constraint
        
        details = {
            "field": field,
            "value": value,
            "constraint": constraint
        }
        
        super().__init__(message, "VALIDATION_ERROR", details)


class ConversationError(TravelAgentException):
    """Raised when conversation management fails."""
    
    def __init__(
        self,
        message: str,
        thread_id: Optional[str] = None,
        conversation_state: Optional[Dict[str, Any]] = None
    ):
        self.thread_id = thread_id
        self.conversation_state = conversation_state
        
        details = {
            "thread_id": thread_id,
            "conversation_state": conversation_state
        }
        
        super().__init__(message, "CONVERSATION_ERROR", details)


class ToolExecutionError(TravelAgentException):
    """Raised when tool execution fails."""
    
    def __init__(
        self,
        message: str,
        tool_name: str,
        tool_args: Optional[Dict[str, Any]] = None,
        execution_time: Optional[float] = None
    ):
        self.tool_name = tool_name
        self.tool_args = tool_args
        self.execution_time = execution_time
        
        details = {
            "tool_name": tool_name,
            "tool_args": tool_args,
            "execution_time": execution_time
        }
        
        super().__init__(message, "TOOL_EXECUTION_ERROR", details)


# Exception mapping for HTTP status codes
EXCEPTION_STATUS_MAP = {
    ConfigurationError: 500,
    ExternalAPIError: 502,
    SerpAPIError: 502,
    OpenAIError: 502,
    AgentError: 500,
    FlightSearchError: 400,
    ParameterExtractionError: 400,
    RateLimitError: 429,
    AuthenticationError: 401,
    AuthorizationError: 403,
    ValidationError: 422,
    ConversationError: 400,
    ToolExecutionError: 500,
    TravelAgentException: 500,
}


def get_http_status_code(exception: Exception) -> int:
    """Get the appropriate HTTP status code for an exception."""
    return EXCEPTION_STATUS_MAP.get(type(exception), 500)
