"""
Pydantic models for hotel search functionality.
"""

from datetime import date, datetime
from typing import List, Optional, Dict, Any, Literal
from pydantic import BaseModel, Field, field_validator
from enum import Enum


class HotelSortBy(str, Enum):
    """Hotel sorting options."""
    RELEVANCE = "0"
    LOWEST_PRICE = "3"
    HIGHEST_RATING = "8"
    MOST_REVIEWED = "13"


class HotelRating(str, Enum):
    """Hotel rating filter options."""
    THREE_FIVE_PLUS = "7"  # 3.5+
    FOUR_PLUS = "8"        # 4.0+
    FOUR_FIVE_PLUS = "9"   # 4.5+


class HotelClass(str, Enum):
    """Hotel class options."""
    TWO_STAR = "2"
    THREE_STAR = "3"
    FOUR_STAR = "4"
    FIVE_STAR = "5"


class PropertyType(str, Enum):
    """Property type options."""
    HOTEL = "hotel"
    VACATION_RENTAL = "vacation_rental"


class HotelSearchRequest(BaseModel):
    """Request model for hotel search."""
    q: str = Field(..., description="Search query (location, hotel name, etc.)")
    check_in_date: date = Field(..., description="Check-in date in YYYY-MM-DD format")
    check_out_date: date = Field(..., description="Check-out date in YYYY-MM-DD format")
    
    # Guest details
    adults: int = Field(2, ge=1, le=20, description="Number of adults (1-20)")
    children: int = Field(0, ge=0, le=10, description="Number of children (0-10)")
    
    # Search preferences
    currency: str = Field("USD", description="Currency code (e.g., USD, EUR)")
    gl: str = Field("us", description="Country code for localization")
    hl: str = Field("en", description="Language code")
    
    # Filters
    sort_by: HotelSortBy = Field(HotelSortBy.RELEVANCE, description="Sort results by")
    min_price: Optional[int] = Field(None, ge=0, description="Minimum price filter")
    max_price: Optional[int] = Field(None, ge=0, description="Maximum price filter")
    rating: Optional[HotelRating] = Field(None, description="Minimum rating filter")
    hotel_class: Optional[str] = Field(None, description="Hotel class filter (comma-separated)")
    property_types: Optional[str] = Field(None, description="Property types filter (comma-separated)")
    amenities: Optional[str] = Field(None, description="Amenities filter (comma-separated)")
    brands: Optional[str] = Field(None, description="Hotel brands filter (comma-separated)")
    
    # Vacation rental specific
    vacation_rentals: bool = Field(False, description="Search for vacation rentals instead of hotels")
    bedrooms: Optional[int] = Field(None, ge=0, description="Minimum number of bedrooms (vacation rentals)")
    bathrooms: Optional[int] = Field(None, ge=0, description="Minimum number of bathrooms (vacation rentals)")
    
    # Special filters
    free_cancellation: bool = Field(False, description="Show only properties with free cancellation")
    special_offers: bool = Field(False, description="Show only properties with special offers")
    eco_certified: bool = Field(False, description="Show only eco-certified properties")
    
    @field_validator('check_out_date')
    @classmethod
    def validate_check_out_date(cls, v, info):
        if info.data.get('check_in_date') and v <= info.data['check_in_date']:
            raise ValueError("Check-out date must be after check-in date")
        return v

    @field_validator('max_price')
    @classmethod
    def validate_price_range(cls, v, info):
        if v is not None:
            min_price = info.data.get('min_price')
            if min_price is not None and v <= min_price:
                raise ValueError("Maximum price must be greater than minimum price")
        return v


class GPSCoordinates(BaseModel):
    """GPS coordinates."""
    latitude: float
    longitude: float


class Transportation(BaseModel):
    """Transportation information."""
    type: str = Field(..., description="Type of transportation (e.g., Taxi, Walking, Public transport)")
    duration: str = Field(..., description="Travel duration (e.g., 30 min)")


class NearbyPlace(BaseModel):
    """Nearby place information."""
    name: str
    transportations: List[Transportation] = Field(default_factory=list)


class HotelImage(BaseModel):
    """Hotel image information."""
    thumbnail: str
    original_image: str


class RateInfo(BaseModel):
    """Rate information."""
    lowest: Optional[str] = None
    extracted_lowest: Optional[float] = None
    before_taxes_fees: Optional[str] = None
    extracted_before_taxes_fees: Optional[float] = None


class PriceSource(BaseModel):
    """Price source information."""
    source: str
    logo: Optional[str] = None
    num_guests: Optional[int] = None
    rate_per_night: Optional[RateInfo] = None


class RatingBreakdown(BaseModel):
    """Rating breakdown by category."""
    name: str
    description: Optional[str] = None
    total_mentioned: Optional[int] = None
    positive: Optional[int] = None
    negative: Optional[int] = None
    neutral: Optional[int] = None


class StarRating(BaseModel):
    """Star rating distribution."""
    stars: int = Field(..., ge=1, le=5)
    count: int = Field(..., ge=0)


class HotelProperty(BaseModel):
    """Hotel property information."""
    type: str = Field(..., description="Type of property (hotel or vacation rental)")
    name: str
    description: Optional[str] = None
    link: Optional[str] = None
    logo: Optional[str] = None
    sponsored: bool = Field(False, description="Whether the property is sponsored")
    eco_certified: bool = Field(False, description="Whether the property is eco-certified")
    
    # Location
    gps_coordinates: Optional[GPSCoordinates] = None
    nearby_places: List[NearbyPlace] = Field(default_factory=list)
    
    # Check-in/out times
    check_in_time: Optional[str] = None
    check_out_time: Optional[str] = None
    
    # Pricing
    rate_per_night: Optional[RateInfo] = None
    total_rate: Optional[RateInfo] = None
    prices: List[PriceSource] = Field(default_factory=list)
    
    # Property details
    hotel_class: Optional[str] = None
    extracted_hotel_class: Optional[int] = None
    images: List[HotelImage] = Field(default_factory=list)
    
    # Ratings and reviews
    overall_rating: Optional[float] = None
    reviews: Optional[int] = None
    ratings: List[StarRating] = Field(default_factory=list)
    location_rating: Optional[float] = None
    reviews_breakdown: List[RatingBreakdown] = Field(default_factory=list)
    
    # Amenities
    amenities: List[str] = Field(default_factory=list)
    excluded_amenities: List[str] = Field(default_factory=list)
    
    # Vacation rental specific
    essential_info: List[str] = Field(default_factory=list)
    
    # Tokens for details
    property_token: Optional[str] = None
    serpapi_property_details_link: Optional[str] = None


class HotelAd(BaseModel):
    """Hotel advertisement information."""
    name: str
    source: str
    source_icon: Optional[str] = None
    link: str
    property_token: Optional[str] = None
    serpapi_property_details_link: Optional[str] = None
    gps_coordinates: Optional[GPSCoordinates] = None
    hotel_class: Optional[int] = None
    thumbnail: Optional[str] = None
    overall_rating: Optional[float] = None
    reviews: Optional[int] = None
    price: Optional[str] = None
    extracted_price: Optional[float] = None
    amenities: List[str] = Field(default_factory=list)
    free_cancellation: bool = Field(False)


class HotelBrand(BaseModel):
    """Hotel brand information."""
    id: int
    name: str
    children: Optional[List['HotelBrand']] = None


class HotelSearchResponse(BaseModel):
    """Response model for hotel search."""
    properties: List[HotelProperty] = Field(default_factory=list)
    ads: List[HotelAd] = Field(default_factory=list)
    brands: List[HotelBrand] = Field(default_factory=list)
    search_metadata: Dict[str, Any] = Field(default_factory=dict)
    search_information: Dict[str, Any] = Field(default_factory=dict)
    serpapi_pagination: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


class HotelSearchParams(BaseModel):
    """Extracted hotel search parameters from user query."""
    location: Optional[str] = None
    check_in_date: Optional[str] = None
    check_out_date: Optional[str] = None
    guests: int = 2
    rooms: int = 1
    hotel_class: Optional[str] = None
    amenities: Optional[str] = None
    max_price: Optional[int] = None
    vacation_rental: bool = False

    def to_search_request(self) -> Optional[HotelSearchRequest]:
        """Convert to HotelSearchRequest if all required fields are present."""
        if not all([self.location, self.check_in_date, self.check_out_date]):
            return None

        try:
            # Convert string dates to date objects
            check_in = datetime.strptime(self.check_in_date, "%Y-%m-%d").date()
            check_out = datetime.strptime(self.check_out_date, "%Y-%m-%d").date()

            return HotelSearchRequest(
                q=self.location,
                check_in_date=check_in,
                check_out_date=check_out,
                adults=self.guests,
                vacation_rentals=self.vacation_rental,
                hotel_class=self.hotel_class,
                amenities=self.amenities,
                max_price=self.max_price
            )
        except (ValueError, TypeError):
            return None


class TravelSearchParams(BaseModel):
    """Combined travel search parameters that can handle both flights and hotels."""
    # Common fields
    search_type: Literal["flight", "hotel", "both"] = "both"

    # Flight-specific fields
    departure_location: Optional[str] = None
    arrival_location: Optional[str] = None
    departure_date: Optional[str] = None
    return_date: Optional[str] = None
    passengers: int = 1
    trip_type: str = "round_trip"
    travel_class: str = "economy"

    # Hotel-specific fields
    hotel_location: Optional[str] = None
    check_in_date: Optional[str] = None
    check_out_date: Optional[str] = None
    guests: int = 2
    rooms: int = 1
    hotel_class: Optional[str] = None
    amenities: Optional[str] = None
    max_price: Optional[int] = None
    vacation_rental: bool = False

    def get_flight_params(self) -> Optional['FlightSearchParams']:
        """Extract flight search parameters."""
        if self.search_type in ["flight", "both"]:
            from .flight import FlightSearchParams
            return FlightSearchParams(
                departure_location=self.departure_location,
                arrival_location=self.arrival_location,
                departure_date=self.departure_date,
                return_date=self.return_date,
                passengers=self.passengers,
                trip_type=self.trip_type,
                travel_class=self.travel_class
            )
        return None

    def get_hotel_params(self) -> Optional[HotelSearchParams]:
        """Extract hotel search parameters."""
        if self.search_type in ["hotel", "both"]:
            return HotelSearchParams(
                location=self.hotel_location,
                check_in_date=self.check_in_date,
                check_out_date=self.check_out_date,
                guests=self.guests,
                rooms=self.rooms,
                hotel_class=self.hotel_class,
                amenities=self.amenities,
                max_price=self.max_price,
                vacation_rental=self.vacation_rental
            )
        return None


class TravelChatResponse(BaseModel):
    """Enhanced response model for travel chat endpoint."""
    message: str = Field(..., description="Assistant response")
    thread_id: str = Field(..., description="Thread ID for conversation continuity")
    flight_results: Optional[Dict[str, Any]] = Field(None, description="Flight search results if applicable")
    hotel_results: Optional[HotelSearchResponse] = Field(None, description="Hotel search results if applicable")
    extracted_params: Optional[TravelSearchParams] = Field(None, description="Extracted travel parameters")
    needs_clarification: bool = Field(False, description="Whether the agent needs more information")
    missing_params: List[str] = Field(default_factory=list, description="List of missing required parameters")
    search_type: Optional[str] = Field(None, description="Type of search performed")


# Enable forward references and rebuild models
HotelBrand.model_rebuild()
TravelChatResponse.model_rebuild()
