"""
Main FastAPI application for the Travel Agent API.
"""

import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from .core.config import get_settings
from .api import chat_router, health_router
from .models.base import ErrorResponse, ValidationError, ValidationErrorResponse

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Application lifespan manager.
    
    Handles startup and shutdown events.
    """
    # Startup
    logger.info("Starting Travel Agent API...")
    
    # Initialize services
    try:
        settings = get_settings()
        logger.info(f"API configuration loaded: {settings.api_title} v{settings.api_version}")
        
        # Test external API connections
        if settings.openai_api_key and settings.serpapi_api_key:
            logger.info("External API keys configured")
        else:
            logger.warning("Some external API keys are missing")
        
        logger.info("Travel Agent API started successfully")
        
    except Exception as e:
        logger.error(f"Failed to start application: {e}")
        raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down Travel Agent API...")
    logger.info("Travel Agent API shutdown complete")


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    
    settings = get_settings()
    api_config = settings.get_api_config()
    
    # Create FastAPI app
    app = FastAPI(
        title=api_config.title,
        description=api_config.description,
        version=api_config.version,
        debug=api_config.debug,
        lifespan=lifespan,
        docs_url="/docs" if api_config.debug else None,
        redoc_url="/redoc" if api_config.debug else None,
    )
    
    # Add middleware
    setup_middleware(app, api_config)
    
    # Add exception handlers
    setup_exception_handlers(app)
    
    # Include routers
    app.include_router(health_router)
    app.include_router(chat_router)
    
    # Add root endpoint
    @app.get("/", tags=["root"])
    async def root():
        """Root endpoint with API information."""
        return {
            "name": api_config.title,
            "version": api_config.version,
            "description": api_config.description,
            "docs_url": "/docs" if api_config.debug else None,
            "health_url": "/health"
        }
    
    return app


def setup_middleware(app: FastAPI, api_config) -> None:
    """Setup middleware for the FastAPI application."""
    
    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=api_config.cors_origins,
        allow_credentials=True,
        allow_methods=api_config.cors_methods,
        allow_headers=api_config.cors_headers,
    )
    
    # Trusted host middleware (for production)
    if not api_config.debug:
        app.add_middleware(
            TrustedHostMiddleware,
            allowed_hosts=["*"]  # Configure this properly in production
        )
    
    # Request logging middleware
    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        """Log all HTTP requests."""
        start_time = time.time()
        
        # Get request ID
        request_id = request.headers.get("x-request-id", str(uuid.uuid4()))
        
        # Log request
        logger.info(
            f"Request {request_id}: {request.method} {request.url.path} "
            f"from {request.client.host if request.client else 'unknown'}"
        )
        
        try:
            response = await call_next(request)
            
            # Log response
            process_time = time.time() - start_time
            logger.info(
                f"Response {request_id}: {response.status_code} "
                f"in {process_time:.3f}s"
            )
            
            # Add request ID to response headers
            response.headers["x-request-id"] = request_id
            
            return response
            
        except Exception as e:
            process_time = time.time() - start_time
            logger.error(
                f"Request {request_id} failed after {process_time:.3f}s: {str(e)}"
            )
            raise


def setup_exception_handlers(app: FastAPI) -> None:
    """Setup exception handlers for the FastAPI application."""
    
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        """Handle request validation errors."""
        validation_errors = []
        
        for error in exc.errors():
            validation_errors.append(ValidationError(
                field=".".join(str(loc) for loc in error["loc"]),
                message=error["msg"],
                value=error.get("input")
            ))
        
        logger.warning(f"Validation error for {request.url.path}: {exc.errors()}")
        
        return JSONResponse(
            status_code=422,
            content=ValidationErrorResponse(
                message="Request validation failed",
                validation_errors=validation_errors
            ).dict()
        )
    
    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        """Handle HTTP exceptions."""
        logger.warning(f"HTTP {exc.status_code} for {request.url.path}: {exc.detail}")
        
        return JSONResponse(
            status_code=exc.status_code,
            content=ErrorResponse(
                message=exc.detail,
                error_code=f"HTTP_{exc.status_code}"
            ).dict()
        )
    
    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        """Handle general exceptions."""
        logger.error(f"Unhandled exception for {request.url.path}: {str(exc)}", exc_info=True)
        
        return JSONResponse(
            status_code=500,
            content=ErrorResponse(
                message="Internal server error",
                error_code="INTERNAL_ERROR",
                error_details={"exception": str(exc)} if get_settings().debug else None
            ).dict()
        )


# Import required modules for middleware
import time
import uuid

# Create the app instance
app = create_app()

if __name__ == "__main__":
    import uvicorn
    
    settings = get_settings()
    
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.reload,
        log_level=settings.log_level.lower()
    )
