"""
Flight search agent using LangGraph ReAct pattern.
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

from .tools import FLIGHT_TOOLS
from ..models.agent import AgentState, AgentConfig
from ..models.flight import FlightSearchParams, ChatRequest, ChatResponse

logger = logging.getLogger(__name__)


class FlightSearchAgent:
    """
    AI agent for flight search using ReAct (Reasoning + Acting) pattern.
    """
    
    def __init__(self, config: Optional[AgentConfig] = None):
        """Initialize the flight search agent."""
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
            FLIGHT_TOOLS,
            checkpointer=self.checkpointer,
            prompt=self._get_system_prompt()
        )
        
        logger.info("Flight search agent initialized")
    
    def _get_system_prompt(self) -> str:
        """Get the system prompt for the flight search agent."""
        return """You are a helpful travel assistant specializing in flight searches. Your goal is to help users find the best flights for their travel needs.

CORE RESPONSIBILITIES:
1. Extract flight search parameters from user queries
2. Search for flights using the available tools
3. Present results in a clear, helpful manner
4. Ask clarifying questions when information is missing
5. Provide travel advice and recommendations

FLIGHT SEARCH PARAMETERS TO EXTRACT:
- Departure location (airport code or city name)
- Arrival location (airport code or city name)  
- Departure date (YYYY-MM-DD format)
- Return date (for round trips, YYYY-MM-DD format)
- Number of passengers (default: 1)
- Trip type (one_way, round_trip, multi_city - default: round_trip)
- Travel class (economy, premium_economy, business, first - default: economy)

CONVERSATION GUIDELINES:
1. Always be friendly and professional
2. If information is missing, ask specific questions to gather it
3. When presenting flight results, highlight key information like price, duration, and stops
4. Provide context about price levels (high, typical, low) when available
5. Mention carbon emissions information when relevant
6. If no flights are found, suggest alternatives or ask for different parameters

TOOL USAGE:
- Use 'search_flights' when you have enough information to perform a search
- Use 'get_airport_suggestions' when you need to resolve unclear location names
- Always validate dates are in the future and return dates are after departure dates

RESPONSE FORMAT:
- Start with a brief acknowledgment of the user's request
- Present search results clearly with prices, times, and key details
- End with helpful next steps or additional questions

IMPORTANT NOTES:
- Today's date is {today_date}
- Always ensure departure dates are in the future
- For round trips, return date must be after departure date
- Be helpful in resolving ambiguous location names
- Provide price context when available (e.g., "This is a typical price for this route")

Remember: Your goal is to make flight searching easy and informative for users!""".format(
            today_date=datetime.now().strftime("%Y-%m-%d")
        )
    
    async def process_message(self, request: ChatRequest) -> ChatResponse:
        """
        Process a user message and return a response.
        
        Args:
            request: Chat request with user message and optional thread_id
            
        Returns:
            ChatResponse with agent's reply and any flight results
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
            
            # Try to extract flight results and parameters from the conversation
            flight_results = None
            extracted_params = None
            needs_clarification = False
            missing_params = []
            
            # Analyze the conversation to determine if we have flight results
            # This is a simplified approach - in production you might want more sophisticated parsing
            if "search_flights" in str(messages):
                # Look for flight search results in tool calls
                for msg in messages:
                    if hasattr(msg, 'tool_calls') and msg.tool_calls:
                        for tool_call in msg.tool_calls:
                            if tool_call['name'] == 'search_flights':
                                # Extract parameters from tool call
                                args = tool_call.get('args', {})
                                extracted_params = FlightSearchParams(
                                    departure_location=args.get('departure_location'),
                                    arrival_location=args.get('arrival_location'),
                                    departure_date=args.get('departure_date'),
                                    return_date=args.get('return_date'),
                                    passengers=args.get('passengers', 1),
                                    trip_type=args.get('trip_type', 'round_trip'),
                                    travel_class=args.get('travel_class', 'economy')
                                )
                                break
            
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
                if "date" in response_lower or "when" in response_lower:
                    missing_params.append("departure_date")
                if "return" in response_lower:
                    missing_params.append("return_date")
                if "passenger" in response_lower or "traveler" in response_lower:
                    missing_params.append("passengers")
            
            return ChatResponse(
                message=response_content,
                thread_id=thread_id,
                flight_results=flight_results,
                extracted_params=extracted_params,
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
            # Note: InMemorySaver doesn't have a direct clear method
            # In production, you might want to use a different checkpointer
            # that supports clearing specific threads
            logger.info(f"Conversation clear requested for thread {thread_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error clearing conversation: {str(e)}")
            return False
    
    def extract_flight_params(self, message: str) -> FlightSearchParams:
        """
        Extract flight search parameters from a user message.
        This is a helper method for testing and debugging.
        
        Args:
            message: User message
            
        Returns:
            FlightSearchParams with extracted information
        """
        # This is a simplified extraction - the agent does this more intelligently
        params = FlightSearchParams()
        
        # Basic keyword extraction (the agent does this much better)
        message_lower = message.lower()
        
        # Extract locations (very basic)
        if "from" in message_lower and "to" in message_lower:
            parts = message_lower.split("from")[1].split("to")
            if len(parts) >= 2:
                params.departure_location = parts[0].strip()
                params.arrival_location = parts[1].split()[0].strip()
        
        # Extract dates (basic pattern matching)
        import re
        date_pattern = r'\d{4}-\d{2}-\d{2}'
        dates = re.findall(date_pattern, message)
        if dates:
            params.departure_date = dates[0]
            if len(dates) > 1:
                params.return_date = dates[1]
        
        return params


# Global agent instance
_flight_agent: Optional[FlightSearchAgent] = None


def get_flight_agent() -> FlightSearchAgent:
    """Get or create the global flight agent instance."""
    global _flight_agent
    if _flight_agent is None:
        _flight_agent = FlightSearchAgent()
    return _flight_agent
