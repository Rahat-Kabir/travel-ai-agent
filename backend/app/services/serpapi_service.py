"""
SerpAPI service for flight search functionality.
"""

import os
import logging
from typing import Optional, Dict, Any, List
from serpapi import GoogleSearch
from datetime import datetime

from ..models.flight import (
    FlightSearchRequest,
    FlightSearchResponse,
    FlightOption,
    Flight,
    Airport,
    Layover,
    CarbonEmissions,
    PriceInsights
)

logger = logging.getLogger(__name__)


class SerpAPIService:
    """Service for interacting with SerpAPI Google Flights."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize SerpAPI service."""
        self.api_key = api_key or os.getenv("SERPAPI_API_KEY")
        if not self.api_key:
            raise ValueError("SerpAPI key is required. Set SERPAPI_API_KEY environment variable.")
    
    def search_flights(self, request: FlightSearchRequest) -> FlightSearchResponse:
        """
        Search for flights using SerpAPI.
        
        Args:
            request: Flight search request parameters
            
        Returns:
            FlightSearchResponse with flight results
        """
        try:
            # Build search parameters
            params = self._build_search_params(request)
            
            # Execute search
            search = GoogleSearch(params)
            results = search.get_dict()
            
            # Parse and return results
            return self._parse_results(results)
            
        except Exception as e:
            logger.error(f"Flight search failed: {str(e)}")
            return FlightSearchResponse(
                error=f"Flight search failed: {str(e)}"
            )
    
    def _build_search_params(self, request: FlightSearchRequest) -> Dict[str, Any]:
        """Build SerpAPI search parameters from request."""
        params = {
            "engine": "google_flights",
            "api_key": self.api_key,
            "departure_id": request.departure_id,
            "arrival_id": request.arrival_id,
            "outbound_date": request.outbound_date.strftime("%Y-%m-%d"),
            "currency": "USD",
            "hl": "en"
        }
        
        # Add return date for round trip
        if request.return_date:
            params["return_date"] = request.return_date.strftime("%Y-%m-%d")
        
        # Add trip type
        params["type"] = request.trip_type.value
        
        # Add passenger counts
        if request.adults > 1:
            params["adults"] = request.adults
        if request.children > 0:
            params["children"] = request.children
        if request.infants_in_seat > 0:
            params["infants_in_seat"] = request.infants_in_seat
        if request.infants_on_lap > 0:
            params["infants_on_lap"] = request.infants_on_lap
        
        # Add travel class
        if request.travel_class.value != "1":  # Not economy
            params["travel_class"] = request.travel_class.value
        
        # Add sorting
        if request.sort_by.value != "1":  # Not top flights
            params["sort_by"] = request.sort_by.value
        
        # Add filters
        if request.stops.value != "0":  # Not any stops
            params["stops"] = request.stops.value
        
        if request.max_price:
            params["max_price"] = request.max_price
        
        if request.include_airlines:
            params["include_airlines"] = request.include_airlines
        
        if request.exclude_airlines:
            params["exclude_airlines"] = request.exclude_airlines
        
        if request.max_duration:
            params["max_duration"] = request.max_duration
        
        return params
    
    def _parse_results(self, results: Dict[str, Any]) -> FlightSearchResponse:
        """Parse SerpAPI results into FlightSearchResponse."""
        try:
            # Check for errors
            if "error" in results:
                return FlightSearchResponse(error=results["error"])
            
            # Extract flight results
            best_flights = []
            other_flights = []
            
            # Parse best flights
            if "best_flights" in results:
                best_flights = [
                    self._parse_flight_option(flight_data)
                    for flight_data in results["best_flights"]
                ]
            
            # Parse other flights
            if "other_flights" in results:
                other_flights = [
                    self._parse_flight_option(flight_data)
                    for flight_data in results["other_flights"]
                ]
            
            # Parse price insights
            price_insights = None
            if "price_insights" in results:
                price_insights = self._parse_price_insights(results["price_insights"])
            
            # Extract search metadata
            search_metadata = results.get("search_metadata", {})
            
            return FlightSearchResponse(
                best_flights=best_flights,
                other_flights=other_flights,
                price_insights=price_insights,
                search_metadata=search_metadata
            )
            
        except Exception as e:
            logger.error(f"Failed to parse flight results: {str(e)}")
            return FlightSearchResponse(
                error=f"Failed to parse flight results: {str(e)}"
            )
    
    def _parse_flight_option(self, flight_data: Dict[str, Any]) -> FlightOption:
        """Parse a single flight option from SerpAPI data."""
        # Parse individual flights
        flights = []
        for flight_info in flight_data.get("flights", []):
            flights.append(self._parse_flight(flight_info))
        
        # Parse layovers
        layovers = []
        for layover_info in flight_data.get("layovers", []):
            layovers.append(Layover(
                duration=layover_info["duration"],
                name=layover_info["name"],
                id=layover_info["id"],
                overnight=layover_info.get("overnight", False)
            ))
        
        # Parse carbon emissions
        carbon_emissions = None
        if "carbon_emissions" in flight_data:
            ce_data = flight_data["carbon_emissions"]
            carbon_emissions = CarbonEmissions(
                this_flight=ce_data["this_flight"],
                typical_for_this_route=ce_data["typical_for_this_route"],
                difference_percent=ce_data["difference_percent"]
            )
        
        return FlightOption(
            flights=flights,
            layovers=layovers,
            total_duration=flight_data["total_duration"],
            carbon_emissions=carbon_emissions,
            price=flight_data["price"],
            type=flight_data["type"],
            airline_logo=flight_data.get("airline_logo"),
            extensions=flight_data.get("extensions", []),
            departure_token=flight_data.get("departure_token"),
            booking_token=flight_data.get("booking_token")
        )
    
    def _parse_flight(self, flight_info: Dict[str, Any]) -> Flight:
        """Parse a single flight segment."""
        departure_airport = Airport(
            name=flight_info["departure_airport"]["name"],
            id=flight_info["departure_airport"]["id"],
            time=flight_info["departure_airport"].get("time")
        )
        
        arrival_airport = Airport(
            name=flight_info["arrival_airport"]["name"],
            id=flight_info["arrival_airport"]["id"],
            time=flight_info["arrival_airport"].get("time")
        )
        
        return Flight(
            departure_airport=departure_airport,
            arrival_airport=arrival_airport,
            duration=flight_info["duration"],
            airplane=flight_info.get("airplane"),
            airline=flight_info["airline"],
            airline_logo=flight_info.get("airline_logo"),
            travel_class=flight_info["travel_class"],
            flight_number=flight_info["flight_number"],
            extensions=flight_info.get("extensions", []),
            legroom=flight_info.get("legroom"),
            overnight=flight_info.get("overnight", False),
            often_delayed_by_over_30_min=flight_info.get("often_delayed_by_over_30_min", False)
        )
    
    def _parse_price_insights(self, insights_data: Dict[str, Any]) -> PriceInsights:
        """Parse price insights data."""
        return PriceInsights(
            lowest_price=insights_data["lowest_price"],
            price_level=insights_data["price_level"],
            typical_price_range=insights_data["typical_price_range"],
            price_history=insights_data.get("price_history", [])
        )
    
    def get_airport_suggestions(self, query: str) -> List[Dict[str, str]]:
        """
        Get airport suggestions for a location query.
        This is a simplified implementation - in production you might want
        to use a dedicated airport/location API.
        """
        # Common airport mappings for major cities
        airport_mappings = {
            "new york": [{"code": "JFK", "name": "John F. Kennedy International Airport"},
                        {"code": "LGA", "name": "LaGuardia Airport"},
                        {"code": "EWR", "name": "Newark Liberty International Airport"}],
            "london": [{"code": "LHR", "name": "London Heathrow Airport"},
                      {"code": "LGW", "name": "London Gatwick Airport"},
                      {"code": "STN", "name": "London Stansted Airport"}],
            "paris": [{"code": "CDG", "name": "Charles de Gaulle Airport"},
                     {"code": "ORY", "name": "Paris-Orly Airport"}],
            "tokyo": [{"code": "NRT", "name": "Narita International Airport"},
                     {"code": "HND", "name": "Haneda Airport"}],
            "los angeles": [{"code": "LAX", "name": "Los Angeles International Airport"}],
            "chicago": [{"code": "ORD", "name": "O'Hare International Airport"},
                       {"code": "MDW", "name": "Midway International Airport"}],
            "miami": [{"code": "MIA", "name": "Miami International Airport"}],
            "san francisco": [{"code": "SFO", "name": "San Francisco International Airport"}],
            "boston": [{"code": "BOS", "name": "Logan International Airport"}],
            "washington": [{"code": "DCA", "name": "Ronald Reagan Washington National Airport"},
                          {"code": "IAD", "name": "Washington Dulles International Airport"}]
        }
        
        query_lower = query.lower()
        suggestions = []
        
        for city, airports in airport_mappings.items():
            if query_lower in city or city in query_lower:
                suggestions.extend(airports)
        
        # If no city match, check if it's already an airport code
        if not suggestions and len(query) == 3 and query.isalpha():
            suggestions.append({"code": query.upper(), "name": f"{query.upper()} Airport"})
        
        return suggestions[:5]  # Return top 5 suggestions
