"""
SerpAPI service for hotel search functionality.
"""

import os
import logging
from typing import Optional, Dict, Any, List
from serpapi import GoogleSearch
from datetime import datetime

from ..models.hotel import (
    HotelSearchRequest,
    HotelSearchResponse,
    HotelProperty,
    HotelAd,
    HotelBrand,
    GPSCoordinates,
    Transportation,
    NearbyPlace,
    HotelImage,
    RateInfo,
    PriceSource,
    RatingBreakdown,
    StarRating
)

logger = logging.getLogger(__name__)


class HotelSerpAPIService:
    """Service for interacting with SerpAPI Google Hotels."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize SerpAPI service."""
        self.api_key = api_key or os.getenv("SERPAPI_API_KEY")
        if not self.api_key:
            raise ValueError("SerpAPI key is required. Set SERPAPI_API_KEY environment variable.")
    
    def search_hotels(self, request: HotelSearchRequest) -> HotelSearchResponse:
        """
        Search for hotels using SerpAPI.
        
        Args:
            request: Hotel search request parameters
            
        Returns:
            HotelSearchResponse with hotel results
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
            logger.error(f"Hotel search failed: {str(e)}")
            return HotelSearchResponse(
                error=f"Hotel search failed: {str(e)}"
            )
    
    def _build_search_params(self, request: HotelSearchRequest) -> Dict[str, Any]:
        """Build SerpAPI search parameters from request."""
        params = {
            "engine": "google_hotels",
            "api_key": self.api_key,
            "q": request.q,
            "check_in_date": request.check_in_date.strftime("%Y-%m-%d"),
            "check_out_date": request.check_out_date.strftime("%Y-%m-%d"),
            "adults": request.adults,
            "children": request.children,
            "currency": request.currency,
            "gl": request.gl,
            "hl": request.hl
        }
        
        # Add sorting
        if request.sort_by.value != "0":  # Not relevance
            params["sort_by"] = request.sort_by.value
        
        # Add price filters
        if request.min_price:
            params["min_price"] = request.min_price
        if request.max_price:
            params["max_price"] = request.max_price
        
        # Add rating filter
        if request.rating:
            params["rating"] = request.rating.value
        
        # Add hotel class filter
        if request.hotel_class:
            params["hotel_class"] = request.hotel_class
        
        # Add property types filter
        if request.property_types:
            params["property_types"] = request.property_types
        
        # Add amenities filter
        if request.amenities:
            params["amenities"] = request.amenities
        
        # Add brands filter
        if request.brands:
            params["brands"] = request.brands
        
        # Add vacation rentals flag
        if request.vacation_rentals:
            params["vacation_rentals"] = "true"
        
        # Add vacation rental specific filters
        if request.bedrooms is not None:
            params["bedrooms"] = request.bedrooms
        if request.bathrooms is not None:
            params["bathrooms"] = request.bathrooms
        
        # Add special filters
        if request.free_cancellation:
            params["free_cancellation"] = "true"
        if request.special_offers:
            params["special_offers"] = "true"
        if request.eco_certified:
            params["eco_certified"] = "true"
        
        return params
    
    def _parse_results(self, results: Dict[str, Any]) -> HotelSearchResponse:
        """Parse SerpAPI results into HotelSearchResponse."""
        try:
            # Check for errors
            if "error" in results:
                return HotelSearchResponse(error=results["error"])
            
            # Extract hotel results
            properties = []
            ads = []
            brands = []
            
            # Parse properties
            if "properties" in results:
                properties = [
                    self._parse_hotel_property(property_data)
                    for property_data in results["properties"]
                ]
            
            # Parse ads
            if "ads" in results:
                ads = [
                    self._parse_hotel_ad(ad_data)
                    for ad_data in results["ads"]
                ]
            
            # Parse brands
            if "brands" in results:
                brands = [
                    self._parse_hotel_brand(brand_data)
                    for brand_data in results["brands"]
                ]
            
            # Extract metadata
            search_metadata = results.get("search_metadata", {})
            search_information = results.get("search_information", {})
            serpapi_pagination = results.get("serpapi_pagination")
            
            return HotelSearchResponse(
                properties=properties,
                ads=ads,
                brands=brands,
                search_metadata=search_metadata,
                search_information=search_information,
                serpapi_pagination=serpapi_pagination
            )
            
        except Exception as e:
            logger.error(f"Failed to parse hotel results: {str(e)}")
            return HotelSearchResponse(
                error=f"Failed to parse hotel results: {str(e)}"
            )
    
    def _parse_hotel_property(self, property_data: Dict[str, Any]) -> HotelProperty:
        """Parse a single hotel property from SerpAPI data."""
        # Parse GPS coordinates
        gps_coordinates = None
        if "gps_coordinates" in property_data:
            gps_data = property_data["gps_coordinates"]
            gps_coordinates = GPSCoordinates(
                latitude=gps_data["latitude"],
                longitude=gps_data["longitude"]
            )
        
        # Parse nearby places
        nearby_places = []
        for place_data in property_data.get("nearby_places", []):
            transportations = []
            for transport_data in place_data.get("transportations", []):
                transportations.append(Transportation(
                    type=transport_data["type"],
                    duration=transport_data["duration"]
                ))
            
            nearby_places.append(NearbyPlace(
                name=place_data["name"],
                transportations=transportations
            ))
        
        # Parse rate information
        rate_per_night = None
        if "rate_per_night" in property_data:
            rate_data = property_data["rate_per_night"]
            rate_per_night = RateInfo(
                lowest=rate_data.get("lowest"),
                extracted_lowest=rate_data.get("extracted_lowest"),
                before_taxes_fees=rate_data.get("before_taxes_fees"),
                extracted_before_taxes_fees=rate_data.get("extracted_before_taxes_fees")
            )
        
        total_rate = None
        if "total_rate" in property_data:
            total_data = property_data["total_rate"]
            total_rate = RateInfo(
                lowest=total_data.get("lowest"),
                extracted_lowest=total_data.get("extracted_lowest"),
                before_taxes_fees=total_data.get("before_taxes_fees"),
                extracted_before_taxes_fees=total_data.get("extracted_before_taxes_fees")
            )
        
        # Parse price sources
        prices = []
        for price_data in property_data.get("prices", []):
            rate_info = None
            if "rate_per_night" in price_data:
                rate_data = price_data["rate_per_night"]
                rate_info = RateInfo(
                    lowest=rate_data.get("lowest"),
                    extracted_lowest=rate_data.get("extracted_lowest"),
                    before_taxes_fees=rate_data.get("before_taxes_fees"),
                    extracted_before_taxes_fees=rate_data.get("extracted_before_taxes_fees")
                )
            
            prices.append(PriceSource(
                source=price_data["source"],
                logo=price_data.get("logo"),
                num_guests=price_data.get("num_guests"),
                rate_per_night=rate_info
            ))
        
        # Parse images
        images = []
        for image_data in property_data.get("images", []):
            images.append(HotelImage(
                thumbnail=image_data["thumbnail"],
                original_image=image_data["original_image"]
            ))
        
        # Parse star ratings
        ratings = []
        for rating_data in property_data.get("ratings", []):
            ratings.append(StarRating(
                stars=rating_data["stars"],
                count=rating_data["count"]
            ))
        
        # Parse reviews breakdown
        reviews_breakdown = []
        for review_data in property_data.get("reviews_breakdown", []):
            reviews_breakdown.append(RatingBreakdown(
                name=review_data["name"],
                description=review_data.get("description"),
                total_mentioned=review_data.get("total_mentioned"),
                positive=review_data.get("positive"),
                negative=review_data.get("negative"),
                neutral=review_data.get("neutral")
            ))
        
        return HotelProperty(
            type=property_data["type"],
            name=property_data["name"],
            description=property_data.get("description"),
            link=property_data.get("link"),
            logo=property_data.get("logo"),
            sponsored=property_data.get("sponsored", False),
            eco_certified=property_data.get("eco_certified", False),
            gps_coordinates=gps_coordinates,
            nearby_places=nearby_places,
            check_in_time=property_data.get("check_in_time"),
            check_out_time=property_data.get("check_out_time"),
            rate_per_night=rate_per_night,
            total_rate=total_rate,
            prices=prices,
            hotel_class=property_data.get("hotel_class"),
            extracted_hotel_class=property_data.get("extracted_hotel_class"),
            images=images,
            overall_rating=property_data.get("overall_rating"),
            reviews=property_data.get("reviews"),
            ratings=ratings,
            location_rating=property_data.get("location_rating"),
            reviews_breakdown=reviews_breakdown,
            amenities=property_data.get("amenities", []),
            excluded_amenities=property_data.get("excluded_amenities", []),
            essential_info=property_data.get("essential_info", []),
            property_token=property_data.get("property_token"),
            serpapi_property_details_link=property_data.get("serpapi_property_details_link")
        )

    def _parse_hotel_ad(self, ad_data: Dict[str, Any]) -> HotelAd:
        """Parse a single hotel ad from SerpAPI data."""
        # Parse GPS coordinates
        gps_coordinates = None
        if "gps_coordinates" in ad_data:
            gps_data = ad_data["gps_coordinates"]
            gps_coordinates = GPSCoordinates(
                latitude=gps_data["latitude"],
                longitude=gps_data["longitude"]
            )

        return HotelAd(
            name=ad_data["name"],
            source=ad_data["source"],
            source_icon=ad_data.get("source_icon"),
            link=ad_data["link"],
            property_token=ad_data.get("property_token"),
            serpapi_property_details_link=ad_data.get("serpapi_property_details_link"),
            gps_coordinates=gps_coordinates,
            hotel_class=ad_data.get("hotel_class"),
            thumbnail=ad_data.get("thumbnail"),
            overall_rating=ad_data.get("overall_rating"),
            reviews=ad_data.get("reviews"),
            price=ad_data.get("price"),
            extracted_price=ad_data.get("extracted_price"),
            amenities=ad_data.get("amenities", []),
            free_cancellation=ad_data.get("free_cancellation", False)
        )

    def _parse_hotel_brand(self, brand_data: Dict[str, Any]) -> HotelBrand:
        """Parse a single hotel brand from SerpAPI data."""
        children = None
        if "children" in brand_data:
            children = [
                HotelBrand(
                    id=child_data["id"],
                    name=child_data["name"]
                )
                for child_data in brand_data["children"]
            ]

        return HotelBrand(
            id=brand_data["id"],
            name=brand_data["name"],
            children=children
        )

    def get_hotel_suggestions(self, query: str) -> List[Dict[str, str]]:
        """
        Get hotel location suggestions for a query.
        This is a simplified implementation - in production you might want
        to use a dedicated location API.
        """
        # Common destination mappings
        destination_mappings = {
            "new york": [{"location": "New York, NY", "description": "New York City, United States"},
                        {"location": "Manhattan, New York", "description": "Manhattan, New York City"},
                        {"location": "Brooklyn, New York", "description": "Brooklyn, New York City"}],
            "london": [{"location": "London, UK", "description": "London, United Kingdom"},
                      {"location": "Central London", "description": "Central London, UK"},
                      {"location": "Westminster, London", "description": "Westminster, London"}],
            "paris": [{"location": "Paris, France", "description": "Paris, France"},
                     {"location": "Champs-Élysées, Paris", "description": "Champs-Élysées, Paris"},
                     {"location": "Montmartre, Paris", "description": "Montmartre, Paris"}],
            "tokyo": [{"location": "Tokyo, Japan", "description": "Tokyo, Japan"},
                     {"location": "Shibuya, Tokyo", "description": "Shibuya, Tokyo"},
                     {"location": "Shinjuku, Tokyo", "description": "Shinjuku, Tokyo"}],
            "los angeles": [{"location": "Los Angeles, CA", "description": "Los Angeles, California"},
                           {"location": "Hollywood, Los Angeles", "description": "Hollywood, Los Angeles"},
                           {"location": "Beverly Hills, CA", "description": "Beverly Hills, California"}],
            "miami": [{"location": "Miami, FL", "description": "Miami, Florida"},
                     {"location": "South Beach, Miami", "description": "South Beach, Miami"},
                     {"location": "Miami Beach, FL", "description": "Miami Beach, Florida"}],
            "las vegas": [{"location": "Las Vegas, NV", "description": "Las Vegas, Nevada"},
                         {"location": "Las Vegas Strip", "description": "Las Vegas Strip, Nevada"},
                         {"location": "Downtown Las Vegas", "description": "Downtown Las Vegas, Nevada"}],
            "san francisco": [{"location": "San Francisco, CA", "description": "San Francisco, California"},
                             {"location": "Union Square, San Francisco", "description": "Union Square, San Francisco"},
                             {"location": "Fisherman's Wharf, San Francisco", "description": "Fisherman's Wharf, San Francisco"}],
            "chicago": [{"location": "Chicago, IL", "description": "Chicago, Illinois"},
                       {"location": "Downtown Chicago", "description": "Downtown Chicago, Illinois"},
                       {"location": "Magnificent Mile, Chicago", "description": "Magnificent Mile, Chicago"}],
            "boston": [{"location": "Boston, MA", "description": "Boston, Massachusetts"},
                      {"location": "Back Bay, Boston", "description": "Back Bay, Boston"},
                      {"location": "Cambridge, MA", "description": "Cambridge, Massachusetts"}]
        }

        query_lower = query.lower()
        suggestions = []

        for city, locations in destination_mappings.items():
            if query_lower in city or city in query_lower:
                suggestions.extend(locations)

        # If no city match, create a generic suggestion
        if not suggestions:
            suggestions.append({
                "location": query.title(),
                "description": f"Hotels in {query.title()}"
            })

        return suggestions[:5]  # Return top 5 suggestions


# Global service instance
_hotel_service_instance = None


def get_hotel_service() -> HotelSerpAPIService:
    """Get the global hotel service instance."""
    global _hotel_service_instance
    if _hotel_service_instance is None:
        _hotel_service_instance = HotelSerpAPIService()
    return _hotel_service_instance
