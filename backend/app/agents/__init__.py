"""
Agents package for the Travel Agent API.
"""

from .flight_agent import FlightSearchAgent, get_flight_agent
from .travel_agent import TravelAgent, get_travel_agent
from .tools import (
    FLIGHT_TOOLS,
    HOTEL_TOOLS,
    TRAVEL_TOOLS,
    search_flights,
    get_airport_suggestions,
    search_hotels,
    get_hotel_suggestions
)

__all__ = [
    # Flight agent (legacy)
    "FlightSearchAgent",
    "get_flight_agent",

    # Travel agent (new comprehensive agent)
    "TravelAgent",
    "get_travel_agent",

    # Tool collections
    "FLIGHT_TOOLS",
    "HOTEL_TOOLS",
    "TRAVEL_TOOLS",

    # Individual tools
    "search_flights",
    "get_airport_suggestions",
    "search_hotels",
    "get_hotel_suggestions",
]
