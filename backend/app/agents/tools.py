"""
LangGraph tools for the travel search agent.
"""

import json
import logging
from typing import Dict, Any, List, Optional
from langchain_core.tools import tool
from datetime import datetime, date

from ..services.serpapi_service import SerpAPIService
from ..services.hotel_service import HotelSerpAPIService, get_hotel_service
from ..models.flight import FlightSearchRequest, FlightSearchParams, TripType, TravelClass
from ..models.hotel import HotelSearchRequest, HotelSearchParams, HotelSortBy

logger = logging.getLogger(__name__)

# Initialize SerpAPI service (lazy initialization to handle missing API keys)
serpapi_service = None


def get_serpapi_service() -> SerpAPIService:
    """Get or create the SerpAPI service instance."""
    global serpapi_service
    if serpapi_service is None:
        serpapi_service = SerpAPIService()
    return serpapi_service


@tool
def search_flights(
    departure_location: str,
    arrival_location: str,
    departure_date: str,
    return_date: Optional[str] = None,
    passengers: int = 1,
    trip_type: str = "round_trip",
    travel_class: str = "economy"
) -> str:
    """
    Search for flights using SerpAPI Google Flights.
    
    Args:
        departure_location: Departure airport code (e.g., 'JFK', 'NYC') or city name
        arrival_location: Arrival airport code (e.g., 'LAX', 'Los Angeles') or city name  
        departure_date: Departure date in YYYY-MM-DD format
        return_date: Return date in YYYY-MM-DD format (required for round trip)
        passengers: Number of passengers (default: 1)
        trip_type: Type of trip - 'one_way', 'round_trip', or 'multi_city' (default: 'round_trip')
        travel_class: Travel class - 'economy', 'premium_economy', 'business', or 'first' (default: 'economy')
    
    Returns:
        JSON string with flight search results or error message
    """
    try:
        # Convert locations to airport codes if needed
        departure_code = _resolve_airport_code(departure_location)
        arrival_code = _resolve_airport_code(arrival_location)
        
        if not departure_code:
            return json.dumps({
                "error": f"Could not resolve departure location: {departure_location}. Please provide a valid airport code (e.g., JFK, LAX) or major city name."
            })
        
        if not arrival_code:
            return json.dumps({
                "error": f"Could not resolve arrival location: {arrival_location}. Please provide a valid airport code (e.g., JFK, LAX) or major city name."
            })
        
        # Parse dates
        try:
            outbound_date = datetime.strptime(departure_date, "%Y-%m-%d").date()
        except ValueError:
            return json.dumps({
                "error": f"Invalid departure date format: {departure_date}. Please use YYYY-MM-DD format."
            })
        
        return_date_obj = None
        if return_date:
            try:
                return_date_obj = datetime.strptime(return_date, "%Y-%m-%d").date()
                if return_date_obj <= outbound_date:
                    return json.dumps({
                        "error": "Return date must be after departure date."
                    })
            except ValueError:
                return json.dumps({
                    "error": f"Invalid return date format: {return_date}. Please use YYYY-MM-DD format."
                })
        
        # Validate trip type and return date consistency
        if trip_type == "round_trip" and not return_date_obj:
            return json.dumps({
                "error": "Return date is required for round trip flights."
            })
        
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
        
        # Create search request
        search_request = FlightSearchRequest(
            departure_id=departure_code,
            arrival_id=arrival_code,
            outbound_date=outbound_date,
            return_date=return_date_obj,
            adults=passengers,
            trip_type=trip_type_map.get(trip_type, TripType.ROUND_TRIP),
            travel_class=class_map.get(travel_class, TravelClass.ECONOMY)
        )
        
        # Execute search
        logger.info(f"Searching flights: {departure_code} -> {arrival_code} on {departure_date}")
        response = get_serpapi_service().search_flights(search_request)
        
        if response.error:
            return json.dumps({"error": response.error})
        
        # Format results for the agent
        result = {
            "success": True,
            "search_params": {
                "departure": departure_code,
                "arrival": arrival_code,
                "departure_date": departure_date,
                "return_date": return_date,
                "passengers": passengers,
                "trip_type": trip_type,
                "travel_class": travel_class
            },
            "results_summary": {
                "best_flights_count": len(response.best_flights),
                "other_flights_count": len(response.other_flights),
                "price_range": None
            },
            "best_flights": []
        }
        
        # Add price insights if available
        if response.price_insights:
            result["price_insights"] = {
                "lowest_price": response.price_insights.lowest_price,
                "price_level": response.price_insights.price_level,
                "typical_range": response.price_insights.typical_price_range
            }
            result["results_summary"]["price_range"] = f"${response.price_insights.typical_price_range[0]}-${response.price_insights.typical_price_range[1]}"
        
        # Add top flight options (limit to 3 for readability)
        for flight_option in response.best_flights[:3]:
            flight_summary = {
                "price": flight_option.price,
                "total_duration_hours": round(flight_option.total_duration / 60, 1),
                "stops": len(flight_option.layovers),
                "airlines": list(set([f.airline for f in flight_option.flights])),
                "departure_time": flight_option.flights[0].departure_airport.time if flight_option.flights else None,
                "arrival_time": flight_option.flights[-1].arrival_airport.time if flight_option.flights else None,
            }
            
            if flight_option.carbon_emissions:
                flight_summary["carbon_emissions"] = {
                    "this_flight_kg": round(flight_option.carbon_emissions.this_flight / 1000, 1),
                    "vs_typical": f"{flight_option.carbon_emissions.difference_percent:+d}%"
                }
            
            result["best_flights"].append(flight_summary)
        
        return json.dumps(result, indent=2)
        
    except Exception as e:
        logger.error(f"Flight search tool error: {str(e)}")
        return json.dumps({
            "error": f"Flight search failed: {str(e)}"
        })


@tool
def get_airport_suggestions(location_query: str) -> str:
    """
    Get airport code suggestions for a location.
    
    Args:
        location_query: City name or partial airport information
    
    Returns:
        JSON string with airport suggestions
    """
    try:
        suggestions = get_serpapi_service().get_airport_suggestions(location_query)
        
        if not suggestions:
            return json.dumps({
                "error": f"No airport suggestions found for: {location_query}",
                "suggestions": []
            })
        
        return json.dumps({
            "query": location_query,
            "suggestions": suggestions
        })
        
    except Exception as e:
        logger.error(f"Airport suggestions error: {str(e)}")
        return json.dumps({
            "error": f"Failed to get airport suggestions: {str(e)}",
            "suggestions": []
        })


def _resolve_airport_code(location: str) -> Optional[str]:
    """
    Resolve a location string to an airport code.
    
    Args:
        location: Location string (airport code or city name)
    
    Returns:
        Airport code or None if not found
    """
    # If it's already a 3-letter code, return it
    if len(location) == 3 and location.isalpha():
        return location.upper()
    
    # Try to get suggestions and use the first one
    suggestions = get_serpapi_service().get_airport_suggestions(location)
    if suggestions:
        return suggestions[0]["code"]
    
    return None


@tool
def search_hotels(
    location: str,
    check_in_date: str,
    check_out_date: str,
    guests: int = 2,
    rooms: int = 1,
    sort_by: str = "relevance",
    max_price: Optional[int] = None,
    hotel_class: Optional[str] = None,
    vacation_rental: bool = False
) -> str:
    """
    Search for hotels using SerpAPI Google Hotels.

    Args:
        location: Hotel location (city, address, or landmark)
        check_in_date: Check-in date in YYYY-MM-DD format
        check_out_date: Check-out date in YYYY-MM-DD format
        guests: Number of guests (default: 2)
        rooms: Number of rooms (default: 1)
        sort_by: Sort results by 'relevance', 'price', 'rating', or 'reviews' (default: 'relevance')
        max_price: Maximum price per night filter
        hotel_class: Hotel class filter (e.g., '3,4,5' for 3-5 star hotels)
        vacation_rental: Search for vacation rentals instead of hotels (default: False)

    Returns:
        JSON string with hotel search results or error message
    """
    try:
        # Parse dates
        try:
            check_in = datetime.strptime(check_in_date, "%Y-%m-%d").date()
        except ValueError:
            return json.dumps({
                "error": f"Invalid check-in date format: {check_in_date}. Please use YYYY-MM-DD format."
            })

        try:
            check_out = datetime.strptime(check_out_date, "%Y-%m-%d").date()
        except ValueError:
            return json.dumps({
                "error": f"Invalid check-out date format: {check_out_date}. Please use YYYY-MM-DD format."
            })

        # Validate date range
        if check_out <= check_in:
            return json.dumps({
                "error": "Check-out date must be after check-in date."
            })

        # Map sort options
        sort_map = {
            "relevance": HotelSortBy.RELEVANCE,
            "price": HotelSortBy.LOWEST_PRICE,
            "rating": HotelSortBy.HIGHEST_RATING,
            "reviews": HotelSortBy.MOST_REVIEWED
        }

        # Create search request
        search_request = HotelSearchRequest(
            q=location,
            check_in_date=check_in,
            check_out_date=check_out,
            adults=guests,
            sort_by=sort_map.get(sort_by, HotelSortBy.RELEVANCE),
            max_price=max_price,
            hotel_class=hotel_class,
            vacation_rentals=vacation_rental
        )

        # Execute search
        logger.info(f"Searching hotels: {location} from {check_in_date} to {check_out_date}")
        response = get_hotel_service().search_hotels(search_request)

        if response.error:
            return json.dumps({"error": response.error})

        # Format results for the agent
        result = {
            "success": True,
            "search_params": {
                "location": location,
                "check_in_date": check_in_date,
                "check_out_date": check_out_date,
                "guests": guests,
                "rooms": rooms,
                "sort_by": sort_by,
                "vacation_rental": vacation_rental
            },
            "results_summary": {
                "properties_count": len(response.properties),
                "ads_count": len(response.ads),
                "price_range": None
            },
            "properties": []
        }

        # Calculate price range from properties
        prices = []
        for prop in response.properties:
            if prop.rate_per_night and prop.rate_per_night.extracted_lowest:
                prices.append(prop.rate_per_night.extracted_lowest)

        if prices:
            result["results_summary"]["price_range"] = f"${min(prices):.0f}-${max(prices):.0f}"

        # Add top property options (limit to 3 for readability)
        for property_data in response.properties[:3]:
            property_summary = {
                "name": property_data.name,
                "type": property_data.type,
                "rating": property_data.overall_rating,
                "reviews": property_data.reviews,
                "price_per_night": None,
                "amenities": property_data.amenities[:5] if property_data.amenities else [],  # Top 5 amenities
                "location_rating": property_data.location_rating
            }

            if property_data.rate_per_night:
                if property_data.rate_per_night.lowest:
                    property_summary["price_per_night"] = property_data.rate_per_night.lowest
                elif property_data.rate_per_night.extracted_lowest:
                    property_summary["price_per_night"] = f"${property_data.rate_per_night.extracted_lowest:.0f}"

            if property_data.hotel_class:
                property_summary["hotel_class"] = property_data.hotel_class

            result["properties"].append(property_summary)

        return json.dumps(result, indent=2)

    except Exception as e:
        logger.error(f"Hotel search tool error: {str(e)}")
        return json.dumps({
            "error": f"Hotel search failed: {str(e)}"
        })


@tool
def get_hotel_suggestions(location_query: str) -> str:
    """
    Get hotel location suggestions for a query.

    Args:
        location_query: City name or location description

    Returns:
        JSON string with location suggestions
    """
    try:
        suggestions = get_hotel_service().get_hotel_suggestions(location_query)

        if not suggestions:
            return json.dumps({
                "error": f"No location suggestions found for: {location_query}",
                "suggestions": []
            })

        return json.dumps({
            "query": location_query,
            "suggestions": suggestions
        })

    except Exception as e:
        logger.error(f"Hotel suggestions error: {str(e)}")
        return json.dumps({
            "error": f"Failed to get hotel suggestions: {str(e)}",
            "suggestions": []
        })


# Tool lists for easy import
FLIGHT_TOOLS = [
    search_flights,
    get_airport_suggestions
]

HOTEL_TOOLS = [
    search_hotels,
    get_hotel_suggestions
]

TRAVEL_TOOLS = FLIGHT_TOOLS + HOTEL_TOOLS
