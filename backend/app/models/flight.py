"""
Pydantic models for flight search functionality.
"""

from datetime import date, datetime
from typing import List, Optional, Dict, Any, Literal
from pydantic import BaseModel, Field, validator
from enum import Enum


class TripType(str, Enum):
    """Flight trip types."""
    ONE_WAY = "2"
    ROUND_TRIP = "1"
    MULTI_CITY = "3"


class SortBy(str, Enum):
    """Flight sorting options."""
    TOP_FLIGHTS = "1"
    PRICE = "2"
    DEPARTURE_TIME = "3"
    ARRIVAL_TIME = "4"
    DURATION = "5"
    EMISSIONS = "6"


class Stops(str, Enum):
    """Number of stops options."""
    ANY = "0"
    NONSTOP = "1"
    ONE_STOP_OR_FEWER = "2"
    TWO_STOPS_OR_FEWER = "3"


class TravelClass(str, Enum):
    """Travel class options."""
    ECONOMY = "1"
    PREMIUM_ECONOMY = "2"
    BUSINESS = "3"
    FIRST = "4"


class FlightSearchRequest(BaseModel):
    """Request model for flight search."""
    departure_id: str = Field(..., description="Departure airport code (e.g., 'JFK') or multiple codes separated by comma")
    arrival_id: str = Field(..., description="Arrival airport code (e.g., 'LAX') or multiple codes separated by comma")
    outbound_date: date = Field(..., description="Departure date in YYYY-MM-DD format")
    return_date: Optional[date] = Field(None, description="Return date for round trip flights")
    
    # Passenger details
    adults: int = Field(1, ge=1, le=9, description="Number of adults (1-9)")
    children: int = Field(0, ge=0, le=8, description="Number of children (0-8)")
    infants_in_seat: int = Field(0, ge=0, le=8, description="Number of infants in seat (0-8)")
    infants_on_lap: int = Field(0, ge=0, le=8, description="Number of infants on lap (0-8)")
    
    # Trip preferences
    trip_type: TripType = Field(TripType.ROUND_TRIP, description="Type of trip")
    travel_class: TravelClass = Field(TravelClass.ECONOMY, description="Travel class")
    sort_by: SortBy = Field(SortBy.TOP_FLIGHTS, description="Sort results by")
    
    # Filters
    stops: Stops = Field(Stops.ANY, description="Number of stops")
    max_price: Optional[int] = Field(None, ge=0, description="Maximum price filter")
    include_airlines: Optional[str] = Field(None, description="Comma-separated airline codes to include")
    exclude_airlines: Optional[str] = Field(None, description="Comma-separated airline codes to exclude")
    max_duration: Optional[int] = Field(None, ge=0, description="Maximum flight duration in minutes")
    
    @validator('return_date')
    def validate_return_date(cls, v, values):
        if 'trip_type' in values and values['trip_type'] == TripType.ROUND_TRIP:
            if not v:
                raise ValueError("Return date is required for round trip flights")
            if 'outbound_date' in values and v <= values['outbound_date']:
                raise ValueError("Return date must be after departure date")
        return v

    @validator('include_airlines', 'exclude_airlines')
    def validate_airlines(cls, v):
        if v:
            # Basic validation for airline codes (2-character IATA codes)
            codes = [code.strip().upper() for code in v.split(',')]
            for code in codes:
                if len(code) != 2 or not code.isalnum():
                    raise ValueError(f"Invalid airline code: {code}")
        return v


class Airport(BaseModel):
    """Airport information."""
    name: str
    id: str
    time: Optional[str] = None


class Flight(BaseModel):
    """Individual flight segment."""
    departure_airport: Airport
    arrival_airport: Airport
    duration: int = Field(..., description="Flight duration in minutes")
    airplane: Optional[str] = None
    airline: str
    airline_logo: Optional[str] = None
    travel_class: str
    flight_number: str
    extensions: List[str] = Field(default_factory=list)
    legroom: Optional[str] = None
    overnight: bool = False
    often_delayed_by_over_30_min: bool = False


class Layover(BaseModel):
    """Layover information."""
    duration: int = Field(..., description="Layover duration in minutes")
    name: str
    id: str
    overnight: bool = False


class CarbonEmissions(BaseModel):
    """Carbon emissions information."""
    this_flight: int = Field(..., description="Carbon emissions for this flight in grams")
    typical_for_this_route: int = Field(..., description="Typical emissions for this route in grams")
    difference_percent: int = Field(..., description="Percentage difference from typical")


class FlightOption(BaseModel):
    """Complete flight option with all segments."""
    flights: List[Flight]
    layovers: List[Layover] = Field(default_factory=list)
    total_duration: int = Field(..., description="Total duration including layovers in minutes")
    carbon_emissions: Optional[CarbonEmissions] = None
    price: int = Field(..., description="Price in the specified currency")
    type: str = Field(..., description="Trip type")
    airline_logo: Optional[str] = None
    extensions: List[str] = Field(default_factory=list)
    departure_token: Optional[str] = None
    booking_token: Optional[str] = None


class PriceInsights(BaseModel):
    """Price insights for the flight search."""
    lowest_price: int
    price_level: str
    typical_price_range: List[int] = Field(..., min_items=2, max_items=2)
    price_history: List[List[int]] = Field(default_factory=list)


class FlightSearchResponse(BaseModel):
    """Response model for flight search."""
    best_flights: List[FlightOption] = Field(default_factory=list)
    other_flights: List[FlightOption] = Field(default_factory=list)
    price_insights: Optional[PriceInsights] = None
    search_metadata: Dict[str, Any] = Field(default_factory=dict)
    error: Optional[str] = None


class FlightSearchParams(BaseModel):
    """Extracted flight search parameters from user query."""
    departure_location: Optional[str] = None
    arrival_location: Optional[str] = None
    departure_date: Optional[str] = None
    return_date: Optional[str] = None
    passengers: int = 1
    trip_type: str = "round_trip"
    travel_class: str = "economy"
    
    def to_search_request(self) -> Optional[FlightSearchRequest]:
        """Convert to FlightSearchRequest if all required fields are present."""
        if not all([self.departure_location, self.arrival_location, self.departure_date]):
            return None
            
        try:
            # Convert string dates to date objects
            outbound_date = datetime.strptime(self.departure_date, "%Y-%m-%d").date()
            return_date_obj = None
            if self.return_date:
                return_date_obj = datetime.strptime(self.return_date, "%Y-%m-%d").date()
            
            # Map trip type
            trip_type_map = {
                "one_way": TripType.ONE_WAY,
                "round_trip": TripType.ROUND_TRIP,
                "multi_city": TripType.MULTI_CITY
            }
            
            # Map travel class
            class_map = {
                "economy": TravelClass.ECONOMY,
                "premium_economy": TravelClass.PREMIUM_ECONOMY,
                "business": TravelClass.BUSINESS,
                "first": TravelClass.FIRST
            }
            
            return FlightSearchRequest(
                departure_id=self.departure_location,
                arrival_id=self.arrival_location,
                outbound_date=outbound_date,
                return_date=return_date_obj,
                adults=self.passengers,
                trip_type=trip_type_map.get(self.trip_type, TripType.ROUND_TRIP),
                travel_class=class_map.get(self.travel_class, TravelClass.ECONOMY)
            )
        except (ValueError, TypeError):
            return None


class ChatMessage(BaseModel):
    """Chat message model."""
    role: Literal["user", "assistant", "system"]
    content: str
    timestamp: datetime = Field(default_factory=datetime.now)


class ChatRequest(BaseModel):
    """Request model for chat endpoint."""
    message: str = Field(..., min_length=1, description="User message")
    thread_id: Optional[str] = Field(None, description="Thread ID for conversation continuity")


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""
    message: str = Field(..., description="Assistant response")
    thread_id: str = Field(..., description="Thread ID for conversation continuity")
    flight_results: Optional[FlightSearchResponse] = Field(None, description="Flight search results if applicable")
    hotel_results: Optional[Dict[str, Any]] = Field(None, description="Hotel search results if applicable")
    extracted_params: Optional[Dict[str, Any]] = Field(None, description="Extracted travel parameters")
    needs_clarification: bool = Field(False, description="Whether the agent needs more information")
    missing_params: List[str] = Field(default_factory=list, description="List of missing required parameters")
