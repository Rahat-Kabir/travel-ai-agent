"""
Comprehensive travel agent using LangGraph ReAct pattern.
Handles both flight and hotel searches.
"""

import os
import json
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, date, timedelta

from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import InMemorySaver

from .tools import TRAVEL_TOOLS
from ..models.agent import AgentState, AgentConfig
from ..models.hotel import TravelSearchParams, HotelSearchParams, HotelSearchResponse
from ..models.flight import FlightSearchParams, ChatResponse, FlightSearchResponse

logger = logging.getLogger(__name__)


class TravelAgent:
    """
    AI agent for comprehensive travel search using ReAct (Reasoning + Acting) pattern.
    Handles both flight and hotel searches intelligently.
    """
    
    def __init__(self, config: Optional[AgentConfig] = None):
        """Initialize the travel agent."""
        self.config = config or AgentConfig()
        
        # Initialize the language model
        self.llm = ChatOpenAI(
            model=self.config.model_name,
            temperature=self.config.temperature,
            max_tokens=self.config.max_tokens,
            api_key=os.getenv("OPENAI_API_KEY")
        )
        
        # Initialize checkpointer for conversation state
        self.checkpointer = InMemorySaver()
        
        # Create the ReAct agent
        self.agent = create_react_agent(
            self.llm,
            TRAVEL_TOOLS,
            checkpointer=self.checkpointer,
            prompt=self._get_system_prompt()
        )
        
        logger.info("Travel agent initialized")
    
    def _get_system_prompt(self) -> str:
        """Get the system prompt for the travel agent."""
        return """You are a comprehensive travel assistant that helps users with both flight and hotel searches. Your goal is to provide the best travel solutions for their needs.

CORE RESPONSIBILITIES:
1. Determine whether users need flights, hotels, or both
2. Extract relevant search parameters from user queries
3. Search for flights and/or hotels using available tools
4. Present results in a clear, helpful manner
5. Ask clarifying questions when information is missing
6. Provide travel advice and recommendations

SEARCH TYPE DETECTION:
- Flight searches: Look for keywords like "flight", "fly", "airline", "departure", "arrival", airport codes
- Hotel searches: Look for keywords like "hotel", "stay", "accommodation", "check-in", "check-out", "room"
- Combined searches: When users mention both travel and accommodation needs

FLIGHT SEARCH PARAMETERS:
- Departure location (airport code or city name)
- Arrival location (airport code or city name)  
- Departure date (YYYY-MM-DD format)
- Return date (for round trips, YYYY-MM-DD format)
- Number of passengers (default: 1)
- Trip type (one_way, round_trip, multi_city - default: round_trip)
- Travel class (economy, premium_economy, business, first - default: economy)

HOTEL SEARCH PARAMETERS:
- Location (city, address, or landmark)
- Check-in date (YYYY-MM-DD format)
- Check-out date (YYYY-MM-DD format)
- Number of guests (default: 2)
- Number of rooms (default: 1)
- Hotel preferences (class, amenities, price range)
- Vacation rental preference

CONVERSATION GUIDELINES:
1. Always be friendly and professional
2. Intelligently determine what type of search the user needs
3. If information is missing, ask specific questions to gather it
4. When presenting results, highlight key information like prices, ratings, and important details
5. Provide context about price levels and recommendations when available
6. If no results are found, suggest alternatives or ask for different parameters
7. For complex trips, break down the search into logical components

TOOL USAGE:
- Use 'search_flights' when you have flight search information
- Use 'search_hotels' when you have hotel search information
- Use 'get_airport_suggestions' for unclear flight locations
- Use 'get_hotel_suggestions' for unclear hotel locations
- Always validate dates are in the future and logical

RESPONSE FORMAT:
- Start with a brief acknowledgment of the user's request
- Present search results clearly with prices, times, and key details
- For combined searches, organize flight and hotel results separately
- End with helpful next steps or additional questions

IMPORTANT NOTES:
- Today's date is {today_date}
- Always ensure dates are in the future and logical
- Be helpful in resolving ambiguous location names
- Provide price context and recommendations when available
- Consider the relationship between flight destinations and hotel locations

Remember: Your goal is to make travel planning easy, comprehensive, and informative for users!""".format(
            today_date=datetime.now().strftime("%Y-%m-%d")
        )
    
    async def process_message(self, request) -> ChatResponse:
        """
        Process a user message and return a response.

        Args:
            request: Chat request with user message and optional thread_id

        Returns:
            ChatResponse with agent's reply and any search results
        """
        try:
            # Generate thread_id if not provided
            thread_id = request.thread_id or f"thread_{datetime.now().timestamp()}"
            
            # Configuration for the agent
            config = {"configurable": {"thread_id": thread_id}}
            
            # Prepare input messages
            inputs = {"messages": [HumanMessage(content=request.message)]}
            
            # Invoke the agent
            logger.info(f"Processing message for thread {thread_id}: {request.message[:100]}...")
            result = self.agent.invoke(inputs, config=config)
            
            # Extract the response
            messages = result.get("messages", [])
            if not messages:
                raise ValueError("No response from agent")
            
            # Get the last AI message
            ai_message = None
            for msg in reversed(messages):
                if isinstance(msg, AIMessage):
                    ai_message = msg
                    break
            
            if not ai_message:
                raise ValueError("No AI response found")
            
            response_content = ai_message.content
            
            # Analyze the conversation to extract results and parameters
            flight_results = None
            hotel_results = None
            extracted_params = None
            needs_clarification = False
            missing_params = []

            # Look for tool calls in the conversation to extract results and parameters
            for msg in messages:
                if hasattr(msg, 'tool_calls') and msg.tool_calls:
                    for tool_call in msg.tool_calls:
                        if tool_call['name'] == 'search_flights':
                            # Extract flight search parameters
                            args = tool_call.get('args', {})
                            flight_params = FlightSearchParams(
                                departure_location=args.get('departure_location'),
                                arrival_location=args.get('arrival_location'),
                                departure_date=args.get('departure_date'),
                                return_date=args.get('return_date'),
                                passengers=args.get('passengers', 1),
                                trip_type=args.get('trip_type', 'round_trip'),
                                travel_class=args.get('travel_class', 'economy')
                            )

                            # Create or update travel search params
                            if extracted_params is None:
                                extracted_params = TravelSearchParams(
                                    search_type="flight",
                                    departure_location=flight_params.departure_location,
                                    arrival_location=flight_params.arrival_location,
                                    departure_date=flight_params.departure_date,
                                    return_date=flight_params.return_date,
                                    passengers=flight_params.passengers,
                                    trip_type=flight_params.trip_type,
                                    travel_class=flight_params.travel_class
                                )
                            else:
                                # Update existing params with flight info
                                extracted_params.search_type = "both" if extracted_params.search_type == "hotel" else "flight"
                                extracted_params.departure_location = flight_params.departure_location
                                extracted_params.arrival_location = flight_params.arrival_location
                                extracted_params.departure_date = flight_params.departure_date
                                extracted_params.return_date = flight_params.return_date
                                extracted_params.passengers = flight_params.passengers
                                extracted_params.trip_type = flight_params.trip_type
                                extracted_params.travel_class = flight_params.travel_class

                        elif tool_call['name'] == 'search_hotels':
                            # Extract hotel search parameters
                            args = tool_call.get('args', {})
                            hotel_params = HotelSearchParams(
                                location=args.get('location'),
                                check_in_date=args.get('check_in_date'),
                                check_out_date=args.get('check_out_date'),
                                guests=args.get('guests', 2),
                                rooms=args.get('rooms', 1),
                                hotel_class=args.get('hotel_class'),
                                max_price=args.get('max_price'),
                                vacation_rental=args.get('vacation_rental', False)
                            )

                            # Create or update travel search params
                            if extracted_params is None:
                                extracted_params = TravelSearchParams(
                                    search_type="hotel",
                                    hotel_location=hotel_params.location,
                                    check_in_date=hotel_params.check_in_date,
                                    check_out_date=hotel_params.check_out_date,
                                    guests=hotel_params.guests,
                                    rooms=hotel_params.rooms,
                                    hotel_class=hotel_params.hotel_class,
                                    max_price=hotel_params.max_price,
                                    vacation_rental=hotel_params.vacation_rental
                                )
                            else:
                                # Update existing params with hotel info
                                extracted_params.search_type = "both" if extracted_params.search_type == "flight" else "hotel"
                                extracted_params.hotel_location = hotel_params.location
                                extracted_params.check_in_date = hotel_params.check_in_date
                                extracted_params.check_out_date = hotel_params.check_out_date
                                extracted_params.guests = hotel_params.guests
                                extracted_params.rooms = hotel_params.rooms
                                extracted_params.hotel_class = hotel_params.hotel_class
                                extracted_params.max_price = hotel_params.max_price
                                extracted_params.vacation_rental = hotel_params.vacation_rental
            
            # Check if the agent is asking for more information
            clarification_indicators = [
                "what", "when", "where", "which", "how many",
                "need to know", "please provide", "can you tell me",
                "missing", "require", "specify"
            ]
            
            response_lower = response_content.lower()
            if any(indicator in response_lower for indicator in clarification_indicators):
                needs_clarification = True
                
                # Try to identify missing parameters
                if "departure" in response_lower or "from" in response_lower:
                    missing_params.append("departure_location")
                if "arrival" in response_lower or "destination" in response_lower or "to" in response_lower:
                    missing_params.append("arrival_location")
                if "check-in" in response_lower or "check in" in response_lower:
                    missing_params.append("check_in_date")
                if "check-out" in response_lower or "check out" in response_lower:
                    missing_params.append("check_out_date")
                if "date" in response_lower or "when" in response_lower:
                    missing_params.append("dates")
                if "passenger" in response_lower or "traveler" in response_lower or "guest" in response_lower:
                    missing_params.append("passengers_or_guests")
                if "location" in response_lower or "where" in response_lower:
                    missing_params.append("location")
            
            # Convert extracted_params to dict if it exists
            extracted_params_dict = None
            if extracted_params:
                extracted_params_dict = extracted_params.dict()

            return ChatResponse(
                message=response_content,
                thread_id=thread_id,
                flight_results=flight_results,
                hotel_results=hotel_results,
                extracted_params=extracted_params_dict,
                needs_clarification=needs_clarification,
                missing_params=missing_params
            )
            
        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")
            return ChatResponse(
                message=f"I apologize, but I encountered an error while processing your request: {str(e)}. Please try again or rephrase your question.",
                thread_id=request.thread_id or f"thread_{datetime.now().timestamp()}",
                needs_clarification=True
            )
    
    def get_conversation_state(self, thread_id: str) -> Optional[Dict[str, Any]]:
        """
        Get the current state of a conversation thread.
        
        Args:
            thread_id: Thread identifier
            
        Returns:
            Dictionary with conversation state or None if not found
        """
        try:
            config = {"configurable": {"thread_id": thread_id}}
            state = self.agent.get_state(config)
            
            if state and state.values:
                return {
                    "messages": [
                        {
                            "type": msg.type if hasattr(msg, 'type') else 'unknown',
                            "content": msg.content if hasattr(msg, 'content') else str(msg)
                        }
                        for msg in state.values.get("messages", [])
                    ],
                    "checkpoint_id": state.config.get("checkpoint_id"),
                    "next_steps": state.next
                }
            
            return None
            
        except Exception as e:
            logger.error(f"Error getting conversation state: {str(e)}")
            return None
    
    def clear_conversation(self, thread_id: str) -> bool:
        """
        Clear the conversation history for a thread.
        
        Args:
            thread_id: Thread identifier
            
        Returns:
            True if successful, False otherwise
        """
        try:
            logger.info(f"Conversation clear requested for thread {thread_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error clearing conversation: {str(e)}")
            return False


# Global agent instance
_travel_agent: Optional[TravelAgent] = None


def get_travel_agent() -> TravelAgent:
    """Get or create the global travel agent instance."""
    global _travel_agent
    if _travel_agent is None:
        _travel_agent = TravelAgent()
    return _travel_agent
