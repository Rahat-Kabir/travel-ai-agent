"""
Health check API endpoints.
"""

import os
import logging
from datetime import datetime
from typing import Dict, Any
from fastapi import APIRouter, HTTPException

from ..models.base import HealthResponse
from ..services.serpapi_service import SerpAPIService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/health", tags=["health"])


@router.get("/", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """
    Main health check endpoint.
    
    Returns:
        HealthResponse with service status and dependency checks
    """
    try:
        dependencies = {}
        
        # Check OpenAI API key
        openai_key = os.getenv("OPENAI_API_KEY")
        dependencies["openai"] = "configured" if openai_key else "missing"
        
        # Check SerpAPI key
        serpapi_key = os.getenv("SERPAPI_API_KEY")
        dependencies["serpapi"] = "configured" if serpapi_key else "missing"
        
        # Try to initialize SerpAPI service
        try:
            if serpapi_key:
                serpapi_service = SerpAPIService(serpapi_key)
                dependencies["serpapi_service"] = "healthy"
            else:
                dependencies["serpapi_service"] = "not_configured"
        except Exception as e:
            dependencies["serpapi_service"] = f"error: {str(e)}"
        
        # Check if all critical dependencies are healthy
        critical_deps = ["openai", "serpapi"]
        all_healthy = all(
            dependencies.get(dep) == "configured" 
            for dep in critical_deps
        )
        
        status = "healthy" if all_healthy else "degraded"
        
        return HealthResponse(
            status=status,
            version="1.0.0",
            dependencies=dependencies
        )
        
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return HealthResponse(
            status="unhealthy",
            version="1.0.0",
            dependencies={"error": str(e)}
        )


@router.get("/detailed", response_model=Dict[str, Any])
async def detailed_health_check() -> Dict[str, Any]:
    """
    Detailed health check with more comprehensive information.
    
    Returns:
        Dictionary with detailed health information
    """
    try:
        health_info = {
            "timestamp": datetime.now().isoformat(),
            "service": "travel-agent-backend",
            "version": "1.0.0",
            "status": "healthy",
            "checks": {}
        }
        
        # Environment checks
        env_checks = {
            "OPENAI_API_KEY": bool(os.getenv("OPENAI_API_KEY")),
            "SERPAPI_API_KEY": bool(os.getenv("SERPAPI_API_KEY")),
        }
        health_info["checks"]["environment"] = env_checks
        
        # Service checks
        service_checks = {}
        
        # Test SerpAPI service
        try:
            serpapi_key = os.getenv("SERPAPI_API_KEY")
            if serpapi_key:
                serpapi_service = SerpAPIService(serpapi_key)
                # Try to get airport suggestions as a simple test
                suggestions = serpapi_service.get_airport_suggestions("NYC")
                service_checks["serpapi"] = {
                    "status": "healthy",
                    "test_result": f"Found {len(suggestions)} suggestions for NYC"
                }
            else:
                service_checks["serpapi"] = {
                    "status": "not_configured",
                    "error": "API key not set"
                }
        except Exception as e:
            service_checks["serpapi"] = {
                "status": "error",
                "error": str(e)
            }
        
        health_info["checks"]["services"] = service_checks
        
        # Determine overall status
        all_env_healthy = all(env_checks.values())
        all_services_healthy = all(
            check.get("status") == "healthy" 
            for check in service_checks.values()
        )
        
        if all_env_healthy and all_services_healthy:
            health_info["status"] = "healthy"
        elif any(check.get("status") == "error" for check in service_checks.values()):
            health_info["status"] = "unhealthy"
        else:
            health_info["status"] = "degraded"
        
        return health_info
        
    except Exception as e:
        logger.error(f"Detailed health check failed: {str(e)}")
        return {
            "timestamp": datetime.now().isoformat(),
            "service": "travel-agent-backend",
            "version": "1.0.0",
            "status": "unhealthy",
            "error": str(e)
        }


@router.get("/ready", response_model=Dict[str, str])
async def readiness_check() -> Dict[str, str]:
    """
    Readiness check endpoint for Kubernetes/container orchestration.
    
    Returns:
        Dictionary indicating if the service is ready to serve requests
    """
    try:
        # Check critical dependencies
        openai_key = os.getenv("OPENAI_API_KEY")
        serpapi_key = os.getenv("SERPAPI_API_KEY")
        
        if not openai_key:
            raise HTTPException(
                status_code=503,
                detail="OpenAI API key not configured"
            )
        
        if not serpapi_key:
            raise HTTPException(
                status_code=503,
                detail="SerpAPI key not configured"
            )
        
        return {
            "status": "ready",
            "timestamp": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Readiness check failed: {str(e)}")
        raise HTTPException(
            status_code=503,
            detail=f"Service not ready: {str(e)}"
        )


@router.get("/live", response_model=Dict[str, str])
async def liveness_check() -> Dict[str, str]:
    """
    Liveness check endpoint for Kubernetes/container orchestration.
    
    Returns:
        Dictionary indicating if the service is alive
    """
    return {
        "status": "alive",
        "timestamp": datetime.now().isoformat()
    }
