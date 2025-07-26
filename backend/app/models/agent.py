"""
Agent state models for LangGraph.
"""

from typing import Annotated, Sequence, Dict, Any, Optional, List
from typing_extensions import TypedDict
from datetime import datetime
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from pydantic import BaseModel, Field

from .flight import FlightSearchParams, FlightSearchResponse
from .hotel import HotelSearchParams, HotelSearchResponse, TravelSearchParams


class AgentState(TypedDict):
    """
    State of the unified travel search agent.

    This represents the complete state that gets passed between nodes
    in the LangGraph workflow.
    """
    # Messages are the core of the conversation
    messages: Annotated[Sequence[BaseMessage], add_messages]

    # Travel search context (unified)
    extracted_params: Optional[TravelSearchParams]
    flight_results: Optional[FlightSearchResponse]
    hotel_results: Optional[HotelSearchResponse]

    # Conversation context
    user_intent: Optional[str]  # What the user is trying to do
    missing_params: List[str]   # Parameters still needed
    clarification_needed: bool  # Whether we need to ask for more info

    # Agent reasoning
    current_step: str           # Current step in the process
    reasoning: str              # Agent's reasoning for current action

    # Error handling
    error_message: Optional[str]
    retry_count: int


class AgentConfig(BaseModel):
    """Configuration for the unified travel search agent."""
    
    # Model configuration
    model_name: str = Field(default="gpt-4o", description="LLM model to use")
    temperature: float = Field(default=0.1, description="Model temperature")
    max_tokens: int = Field(default=1000, description="Maximum tokens for response")
    
    # Agent behavior
    max_retries: int = Field(default=3, description="Maximum retries for failed operations")
    enable_clarification: bool = Field(default=True, description="Whether to ask clarifying questions")
    
    # Search preferences
    default_trip_type: str = Field(default="round_trip", description="Default trip type")
    default_travel_class: str = Field(default="economy", description="Default travel class")
    max_results: int = Field(default=10, description="Maximum search results to return")

    # Hotel search preferences
    default_hotel_class: Optional[str] = Field(default=None, description="Default hotel class filter")
    default_guests: int = Field(default=2, description="Default number of guests")
    default_rooms: int = Field(default=1, description="Default number of rooms")
    
    # Conversation settings
    conversation_memory_limit: int = Field(default=20, description="Maximum messages to keep in memory")


class ToolCallResult(BaseModel):
    """Result from a tool call."""
    tool_name: str
    success: bool
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    execution_time: float = 0.0


class AgentMetrics(BaseModel):
    """Metrics for agent performance tracking."""
    
    # Conversation metrics
    total_messages: int = 0
    user_messages: int = 0
    assistant_messages: int = 0
    
    # Tool usage metrics
    tool_calls: int = 0
    successful_tool_calls: int = 0
    failed_tool_calls: int = 0
    
    # Search metrics
    flight_searches: int = 0
    hotel_searches: int = 0
    successful_searches: int = 0
    
    # Performance metrics
    average_response_time: float = 0.0
    total_tokens_used: int = 0
    
    # Error tracking
    errors: List[str] = Field(default_factory=list)
    
    def add_tool_call(self, result: ToolCallResult):
        """Add a tool call result to metrics."""
        self.tool_calls += 1
        if result.success:
            self.successful_tool_calls += 1
        else:
            self.failed_tool_calls += 1
            if result.error:
                self.errors.append(f"{result.tool_name}: {result.error}")
    
    def add_flight_search(self, success: bool, error: Optional[str] = None):
        """Add a flight search result to metrics."""
        self.flight_searches += 1
        if success:
            self.successful_searches += 1
        elif error:
            self.errors.append(f"Flight search: {error}")


class ConversationContext(BaseModel):
    """Context for the current conversation."""
    
    # User information
    user_preferences: Dict[str, Any] = Field(default_factory=dict)
    conversation_history: List[Dict[str, str]] = Field(default_factory=list)
    
    # Current search context
    active_search: Optional[TravelSearchParams] = None
    last_flight_results: Optional[FlightSearchResponse] = None
    last_hotel_results: Optional[HotelSearchResponse] = None
    
    # Conversation state
    awaiting_clarification: bool = False
    clarification_topic: Optional[str] = None
    
    # Session information
    session_start: Optional[str] = None
    last_activity: Optional[str] = None
    
    def add_message(self, role: str, content: str):
        """Add a message to conversation history."""
        self.conversation_history.append({
            "role": role,
            "content": content,
            "timestamp": str(datetime.now())
        })
        
        # Keep only recent messages
        if len(self.conversation_history) > 50:
            self.conversation_history = self.conversation_history[-50:]
    
    def update_search_context(self, params: TravelSearchParams):
        """Update the active search context."""
        self.active_search = params
        self.awaiting_clarification = False
        self.clarification_topic = None
    
    def set_clarification_needed(self, topic: str):
        """Set that clarification is needed on a specific topic."""
        self.awaiting_clarification = True
        self.clarification_topic = topic


# Import datetime for ConversationContext
from datetime import datetime
