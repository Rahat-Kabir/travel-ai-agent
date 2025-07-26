"""
FastAPI dependencies for the Travel Agent API.
"""

import os
import logging
from typing import Optional
from fastapi import Header, HTTPException, Depends

logger = logging.getLogger(__name__)


async def get_current_user_id(
    authorization: Optional[str] = Header(None)
) -> Optional[str]:
    """
    Get the current user ID from the authorization header.
    
    This is a placeholder implementation. In production, you would:
    1. Parse the JWT token from the Authorization header
    2. Validate the token signature
    3. Extract the user ID from the token claims
    4. Handle token expiration and refresh
    
    Args:
        authorization: Authorization header value
    
    Returns:
        User ID if authenticated, None otherwise
    """
    # For now, we'll just return None to allow unauthenticated access
    # In production, implement proper JWT authentication here
    
    if authorization:
        # Basic validation - in production use proper JWT validation
        if authorization.startswith("Bearer "):
            token = authorization[7:]  # Remove "Bearer " prefix
            # TODO: Validate JWT token and extract user ID
            # For now, just return a placeholder user ID
            return f"user_{hash(token) % 10000}"
    
    return None


async def get_api_key(
    x_api_key: Optional[str] = Header(None)
) -> Optional[str]:
    """
    Get API key from header for API key authentication.
    
    Args:
        x_api_key: API key from X-API-Key header
    
    Returns:
        API key if provided
    """
    return x_api_key


async def validate_api_key(
    api_key: Optional[str] = Depends(get_api_key)
) -> str:
    """
    Validate API key for protected endpoints.
    
    Args:
        api_key: API key from header
    
    Returns:
        Validated API key
    
    Raises:
        HTTPException: If API key is invalid or missing
    """
    if not api_key:
        raise HTTPException(
            status_code=401,
            detail="API key required",
            headers={"WWW-Authenticate": "ApiKey"}
        )
    
    # In production, validate against a database or configuration
    valid_api_keys = os.getenv("VALID_API_KEYS", "").split(",")
    valid_api_keys = [key.strip() for key in valid_api_keys if key.strip()]
    
    if valid_api_keys and api_key not in valid_api_keys:
        raise HTTPException(
            status_code=401,
            detail="Invalid API key",
            headers={"WWW-Authenticate": "ApiKey"}
        )
    
    return api_key


async def get_rate_limit_key(
    user_id: Optional[str] = Depends(get_current_user_id),
    api_key: Optional[str] = Depends(get_api_key)
) -> str:
    """
    Get a key for rate limiting based on user ID or API key.
    
    Args:
        user_id: Current user ID
        api_key: API key
    
    Returns:
        Rate limit key
    """
    if user_id:
        return f"user:{user_id}"
    elif api_key:
        return f"api_key:{api_key}"
    else:
        return "anonymous"


class RateLimiter:
    """
    Simple in-memory rate limiter.
    In production, use Redis or a proper rate limiting service.
    """
    
    def __init__(self):
        self.requests = {}
    
    def is_allowed(self, key: str, limit: int = 100, window: int = 3600) -> bool:
        """
        Check if a request is allowed based on rate limits.
        
        Args:
            key: Rate limit key
            limit: Maximum requests per window
            window: Time window in seconds
        
        Returns:
            True if request is allowed, False otherwise
        """
        import time
        
        now = time.time()
        window_start = now - window
        
        # Clean old requests
        if key in self.requests:
            self.requests[key] = [
                req_time for req_time in self.requests[key]
                if req_time > window_start
            ]
        else:
            self.requests[key] = []
        
        # Check if limit exceeded
        if len(self.requests[key]) >= limit:
            return False
        
        # Add current request
        self.requests[key].append(now)
        return True


# Global rate limiter instance
rate_limiter = RateLimiter()


async def check_rate_limit(
    rate_limit_key: str = Depends(get_rate_limit_key)
) -> None:
    """
    Check rate limits for the current request.
    
    Args:
        rate_limit_key: Rate limit key
    
    Raises:
        HTTPException: If rate limit exceeded
    """
    # Get rate limit settings from environment
    rate_limit = int(os.getenv("RATE_LIMIT_REQUESTS", "100"))
    rate_window = int(os.getenv("RATE_LIMIT_WINDOW", "3600"))
    
    if not rate_limiter.is_allowed(rate_limit_key, rate_limit, rate_window):
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded",
            headers={
                "Retry-After": str(rate_window),
                "X-RateLimit-Limit": str(rate_limit),
                "X-RateLimit-Window": str(rate_window)
            }
        )


async def get_request_id(
    x_request_id: Optional[str] = Header(None)
) -> str:
    """
    Get or generate a request ID for tracing.
    
    Args:
        x_request_id: Request ID from header
    
    Returns:
        Request ID
    """
    if x_request_id:
        return x_request_id
    
    # Generate a new request ID
    import uuid
    return str(uuid.uuid4())


# Common dependencies for protected endpoints
async def get_authenticated_user(
    user_id: Optional[str] = Depends(get_current_user_id)
) -> str:
    """
    Ensure user is authenticated.
    
    Args:
        user_id: Current user ID
    
    Returns:
        User ID
    
    Raises:
        HTTPException: If user is not authenticated
    """
    if not user_id:
        raise HTTPException(
            status_code=401,
            detail="Authentication required",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    return user_id
