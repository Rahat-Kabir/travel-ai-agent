"""
Chat API endpoints for the travel agent.
"""

import logging
from typing import Dict, Any, Optional
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse

from ..models.flight import ChatRequest, ChatResponse
from ..models.hotel import HotelSearchRequest, HotelSearchResponse
from ..models.base import BaseResponse, ErrorResponse, ResponseStatus
from ..agents import get_travel_agent
from ..core.dependencies import get_current_user_id

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/message", response_model=ChatResponse)
async def send_message(
    request: ChatRequest,
    user_id: Optional[str] = Depends(get_current_user_id)
) -> ChatResponse:
    """
    Send a message to the travel agent.

    Args:
        request: Chat request with user message and optional thread_id
        user_id: Current user ID (from authentication, optional for now)

    Returns:
        ChatResponse with agent's reply and any search results
    """
    try:
        logger.info(f"Received chat message: {request.message[:100]}...")

        # Get the unified travel agent
        agent = get_travel_agent()

        # Process the message
        response = await agent.process_message(request)

        logger.info(f"Agent response generated for thread {response.thread_id}")
        return response

    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process message: {str(e)}"
        )


@router.post("/flight-message", response_model=ChatResponse)
async def send_flight_message(
    request: ChatRequest,
    user_id: Optional[str] = Depends(get_current_user_id)
) -> ChatResponse:
    """
    Send a message to the flight search agent (legacy endpoint for backward compatibility).

    Args:
        request: Chat request with user message and optional thread_id
        user_id: Current user ID (from authentication, optional for now)

    Returns:
        ChatResponse with agent's reply and flight results
    """
    try:
        logger.info(f"Received flight chat message: {request.message[:100]}...")

        # Get the unified travel agent
        agent = get_travel_agent()

        # Process the message
        response = await agent.process_message(request)

        logger.info(f"Flight agent response generated for thread {response.thread_id}")
        return response

    except Exception as e:
        logger.error(f"Error in flight chat endpoint: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process flight message: {str(e)}"
        )


@router.post("/hotel-search", response_model=HotelSearchResponse)
async def search_hotels_direct(
    request: HotelSearchRequest,
    user_id: Optional[str] = Depends(get_current_user_id)
) -> HotelSearchResponse:
    """
    Direct hotel search endpoint (for testing and API documentation).

    Args:
        request: Hotel search request with location, dates, and preferences
        user_id: Current user ID (from authentication, optional for now)

    Returns:
        HotelSearchResponse with hotel search results
    """
    try:
        logger.info(f"Direct hotel search: {request.q} from {request.check_in_date} to {request.check_out_date}")

        # Import hotel service
        from ..services.hotel_service import HotelService

        # Create hotel service instance
        hotel_service = HotelService()

        # Perform hotel search
        response = hotel_service.search_hotels(request)

        logger.info(f"Hotel search completed with {len(response.properties)} properties found")
        return response

    except Exception as e:
        logger.error(f"Error in hotel search endpoint: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to search hotels: {str(e)}"
        )


@router.get("/conversation/{thread_id}", response_model=Dict[str, Any])
async def get_conversation_state(
    thread_id: str,
    user_id: Optional[str] = Depends(get_current_user_id)
) -> Dict[str, Any]:
    """
    Get the current state of a conversation thread.

    Args:
        thread_id: Thread identifier
        user_id: Current user ID (from authentication, optional for now)

    Returns:
        Dictionary with conversation state
    """
    try:
        # Use travel agent by default
        agent = get_travel_agent()
        state = agent.get_conversation_state(thread_id)

        if state is None:
            raise HTTPException(
                status_code=404,
                detail=f"Conversation thread {thread_id} not found"
            )

        return {
            "status": "success",
            "thread_id": thread_id,
            "conversation_state": state
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting conversation state: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get conversation state: {str(e)}"
        )


@router.delete("/conversation/{thread_id}", response_model=BaseResponse)
async def clear_conversation(
    thread_id: str,
    user_id: Optional[str] = Depends(get_current_user_id)
) -> BaseResponse:
    """
    Clear the conversation history for a thread.

    Args:
        thread_id: Thread identifier
        user_id: Current user ID (from authentication, optional for now)

    Returns:
        BaseResponse indicating success or failure
    """
    try:
        # Use travel agent by default
        agent = get_travel_agent()
        success = agent.clear_conversation(thread_id)

        if success:
            return BaseResponse(
                status=ResponseStatus.SUCCESS,
                message=f"Conversation {thread_id} cleared successfully"
            )
        else:
            return BaseResponse(
                status=ResponseStatus.ERROR,
                message=f"Failed to clear conversation {thread_id}"
            )

    except Exception as e:
        logger.error(f"Error clearing conversation: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to clear conversation: {str(e)}"
        )


@router.post("/extract-params", response_model=Dict[str, Any])
async def extract_flight_params(
    request: Dict[str, str],
    user_id: Optional[str] = Depends(get_current_user_id)
) -> Dict[str, Any]:
    """
    Extract flight search parameters from a message (for testing/debugging).
    
    Args:
        request: Dictionary with 'message' key
        user_id: Current user ID (from authentication, optional for now)
    
    Returns:
        Dictionary with extracted parameters
    """
    try:
        message = request.get("message", "")
        if not message:
            raise HTTPException(
                status_code=400,
                detail="Message is required"
            )
        
        agent = get_travel_agent()
        params = agent.extract_flight_params(message)
        
        return {
            "status": "success",
            "message": message,
            "extracted_params": params.dict()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error extracting parameters: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to extract parameters: {str(e)}"
        )


@router.get("/health", response_model=Dict[str, str])
async def chat_health() -> Dict[str, str]:
    """
    Health check endpoint for the chat service.

    Returns:
        Dictionary with health status
    """
    try:
        # Try to get the travel agent to ensure it's working
        agent = get_travel_agent()

        return {
            "status": "healthy",
            "service": "travel-chat",
            "agent_model": agent.config.model_name,
            "capabilities": "flights,hotels",
            "timestamp": str(logger.handlers[0].formatter.formatTime(logger.makeRecord(
                "health", logging.INFO, "", 0, "", (), None
            )) if logger.handlers else "unknown")
        }

    except Exception as e:
        logger.error(f"Chat health check failed: {str(e)}")
        return {
            "status": "unhealthy",
            "service": "travel-chat",
            "error": str(e)
        }
