import 'package:json_annotation/json_annotation.dart';

part 'hotel_models.g.dart';

enum HotelSortBy {
  @JsonValue('0')
  relevance,
  @JsonValue('3')
  lowestPrice,
  @JsonValue('8')
  highestRating,
  @JsonValue('13')
  mostReviewed,
}

enum HotelRating {
  @JsonValue('7')
  threeFivePlus,
  @JsonValue('8')
  fourPlus,
  @JsonValue('9')
  fourFivePlus,
}

enum HotelClass {
  @JsonValue('2')
  twoStar,
  @JsonValue('3')
  threeStar,
  @JsonValue('4')
  fourStar,
  @JsonValue('5')
  fiveStar,
}

enum PropertyType {
  @JsonValue('hotel')
  hotel,
  @JsonValue('vacation_rental')
  vacationRental,
}

@JsonSerializable()
class GPSCoordinates {
  final double latitude;
  final double longitude;

  GPSCoordinates({
    required this.latitude,
    required this.longitude,
  });

  factory GPSCoordinates.fromJson(Map<String, dynamic> json) =>
      _$GPSCoordinatesFromJson(json);

  Map<String, dynamic> toJson() => _$GPSCoordinatesToJson(this);
}

@JsonSerializable()
class Transportation {
  final String type;
  final String duration;

  Transportation({
    required this.type,
    required this.duration,
  });

  factory Transportation.fromJson(Map<String, dynamic> json) =>
      _$TransportationFromJson(json);

  Map<String, dynamic> toJson() => _$TransportationToJson(this);
}

@JsonSerializable()
class NearbyPlace {
  final String name;
  final List<Transportation> transportations;

  NearbyPlace({
    required this.name,
    this.transportations = const [],
  });

  factory NearbyPlace.fromJson(Map<String, dynamic> json) =>
      _$NearbyPlaceFromJson(json);

  Map<String, dynamic> toJson() => _$NearbyPlaceToJson(this);
}

@JsonSerializable()
class HotelImage {
  final String thumbnail;
  @JsonKey(name: 'original_image')
  final String originalImage;

  HotelImage({
    required this.thumbnail,
    required this.originalImage,
  });

  factory HotelImage.fromJson(Map<String, dynamic> json) =>
      _$HotelImageFromJson(json);

  Map<String, dynamic> toJson() => _$HotelImageToJson(this);
}

@JsonSerializable()
class RateInfo {
  final String? lowest;
  @JsonKey(name: 'extracted_lowest')
  final double? extractedLowest;
  @JsonKey(name: 'before_taxes_fees')
  final String? beforeTaxesFees;
  @JsonKey(name: 'extracted_before_taxes_fees')
  final double? extractedBeforeTaxesFees;

  RateInfo({
    this.lowest,
    this.extractedLowest,
    this.beforeTaxesFees,
    this.extractedBeforeTaxesFees,
  });

  factory RateInfo.fromJson(Map<String, dynamic> json) =>
      _$RateInfoFromJson(json);

  Map<String, dynamic> toJson() => _$RateInfoToJson(this);
}

@JsonSerializable()
class PriceSource {
  final String source;
  final String? logo;
  @JsonKey(name: 'num_guests')
  final int? numGuests;
  @JsonKey(name: 'rate_per_night')
  final RateInfo? ratePerNight;

  PriceSource({
    required this.source,
    this.logo,
    this.numGuests,
    this.ratePerNight,
  });

  factory PriceSource.fromJson(Map<String, dynamic> json) =>
      _$PriceSourceFromJson(json);

  Map<String, dynamic> toJson() => _$PriceSourceToJson(this);
}

@JsonSerializable()
class RatingBreakdown {
  final String name;
  final String? description;
  @JsonKey(name: 'total_mentioned')
  final int? totalMentioned;
  final int? positive;
  final int? negative;
  final int? neutral;

  RatingBreakdown({
    required this.name,
    this.description,
    this.totalMentioned,
    this.positive,
    this.negative,
    this.neutral,
  });

  factory RatingBreakdown.fromJson(Map<String, dynamic> json) =>
      _$RatingBreakdownFromJson(json);

  Map<String, dynamic> toJson() => _$RatingBreakdownToJson(this);
}

@JsonSerializable()
class StarRating {
  final int stars;
  final int count;

  StarRating({
    required this.stars,
    required this.count,
  });

  factory StarRating.fromJson(Map<String, dynamic> json) =>
      _$StarRatingFromJson(json);

  Map<String, dynamic> toJson() => _$StarRatingToJson(this);
}

@JsonSerializable()
class HotelProperty {
  final String type;
  final String name;
  final String? description;
  final String? link;
  final String? logo;
  final bool sponsored;
  @JsonKey(name: 'eco_certified')
  final bool ecoCertified;

  // Location
  @JsonKey(name: 'gps_coordinates')
  final GPSCoordinates? gpsCoordinates;
  @JsonKey(name: 'nearby_places')
  final List<NearbyPlace> nearbyPlaces;

  // Check-in/out times
  @JsonKey(name: 'check_in_time')
  final String? checkInTime;
  @JsonKey(name: 'check_out_time')
  final String? checkOutTime;

  // Pricing
  @JsonKey(name: 'rate_per_night')
  final RateInfo? ratePerNight;
  @JsonKey(name: 'total_rate')
  final RateInfo? totalRate;
  final List<PriceSource> prices;

  // Property details
  @JsonKey(name: 'hotel_class')
  final String? hotelClass;
  @JsonKey(name: 'extracted_hotel_class')
  final int? extractedHotelClass;
  final List<HotelImage> images;

  // Ratings and reviews
  @JsonKey(name: 'overall_rating')
  final double? overallRating;
  final int? reviews;
  final List<StarRating> ratings;
  @JsonKey(name: 'location_rating')
  final double? locationRating;
  @JsonKey(name: 'reviews_breakdown')
  final List<RatingBreakdown> reviewsBreakdown;

  // Amenities
  final List<String> amenities;
  @JsonKey(name: 'excluded_amenities')
  final List<String> excludedAmenities;

  // Vacation rental specific
  @JsonKey(name: 'essential_info')
  final List<String> essentialInfo;

  // Tokens for details
  @JsonKey(name: 'property_token')
  final String? propertyToken;
  @JsonKey(name: 'serpapi_property_details_link')
  final String? serpapiPropertyDetailsLink;

  HotelProperty({
    required this.type,
    required this.name,
    this.description,
    this.link,
    this.logo,
    this.sponsored = false,
    this.ecoCertified = false,
    this.gpsCoordinates,
    this.nearbyPlaces = const [],
    this.checkInTime,
    this.checkOutTime,
    this.ratePerNight,
    this.totalRate,
    this.prices = const [],
    this.hotelClass,
    this.extractedHotelClass,
    this.images = const [],
    this.overallRating,
    this.reviews,
    this.ratings = const [],
    this.locationRating,
    this.reviewsBreakdown = const [],
    this.amenities = const [],
    this.excludedAmenities = const [],
    this.essentialInfo = const [],
    this.propertyToken,
    this.serpapiPropertyDetailsLink,
  });

  factory HotelProperty.fromJson(Map<String, dynamic> json) =>
      _$HotelPropertyFromJson(json);

  Map<String, dynamic> toJson() => _$HotelPropertyToJson(this);
}

@JsonSerializable()
class HotelAd {
  final String name;
  final String source;
  @JsonKey(name: 'source_icon')
  final String? sourceIcon;
  final String link;
  @JsonKey(name: 'property_token')
  final String? propertyToken;
  @JsonKey(name: 'serpapi_property_details_link')
  final String? serpapiPropertyDetailsLink;
  @JsonKey(name: 'gps_coordinates')
  final GPSCoordinates? gpsCoordinates;
  @JsonKey(name: 'hotel_class')
  final int? hotelClass;
  final String? thumbnail;
  @JsonKey(name: 'overall_rating')
  final double? overallRating;
  final int? reviews;
  final String? price;
  @JsonKey(name: 'extracted_price')
  final double? extractedPrice;
  final List<String> amenities;
  @JsonKey(name: 'free_cancellation')
  final bool freeCancellation;

  HotelAd({
    required this.name,
    required this.source,
    this.sourceIcon,
    required this.link,
    this.propertyToken,
    this.serpapiPropertyDetailsLink,
    this.gpsCoordinates,
    this.hotelClass,
    this.thumbnail,
    this.overallRating,
    this.reviews,
    this.price,
    this.extractedPrice,
    this.amenities = const [],
    this.freeCancellation = false,
  });

  factory HotelAd.fromJson(Map<String, dynamic> json) =>
      _$HotelAdFromJson(json);

  Map<String, dynamic> toJson() => _$HotelAdToJson(this);
}

@JsonSerializable()
class HotelBrand {
  final int id;
  final String name;
  final List<HotelBrand>? children;

  HotelBrand({
    required this.id,
    required this.name,
    this.children,
  });

  factory HotelBrand.fromJson(Map<String, dynamic> json) =>
      _$HotelBrandFromJson(json);

  Map<String, dynamic> toJson() => _$HotelBrandToJson(this);
}

@JsonSerializable()
class HotelSearchResponse {
  final List<HotelProperty> properties;
  final List<HotelAd> ads;
  final List<HotelBrand> brands;
  @JsonKey(name: 'search_metadata')
  final Map<String, dynamic> searchMetadata;
  @JsonKey(name: 'search_information')
  final Map<String, dynamic> searchInformation;
  @JsonKey(name: 'serpapi_pagination')
  final Map<String, dynamic>? serpapiPagination;
  final String? error;

  HotelSearchResponse({
    this.properties = const [],
    this.ads = const [],
    this.brands = const [],
    this.searchMetadata = const {},
    this.searchInformation = const {},
    this.serpapiPagination,
    this.error,
  });

  factory HotelSearchResponse.fromJson(Map<String, dynamic> json) =>
      _$HotelSearchResponseFromJson(json);

  Map<String, dynamic> toJson() => _$HotelSearchResponseToJson(this);
}

@JsonSerializable()
class HotelSearchRequest {
  final String q;
  @JsonKey(name: 'check_in_date')
  final String checkInDate;
  @JsonKey(name: 'check_out_date')
  final String checkOutDate;
  final int adults;
  final int children;
  final String currency;
  final String gl;
  final String hl;
  @JsonKey(name: 'sort_by')
  final HotelSortBy sortBy;
  @JsonKey(name: 'min_price')
  final int? minPrice;
  @JsonKey(name: 'max_price')
  final int? maxPrice;
  final HotelRating? rating;
  @JsonKey(name: 'hotel_class')
  final String? hotelClass;
  @JsonKey(name: 'property_types')
  final String? propertyTypes;
  final String? amenities;
  final String? brands;
  @JsonKey(name: 'vacation_rentals')
  final bool vacationRentals;
  final int? bedrooms;
  final int? bathrooms;
  @JsonKey(name: 'free_cancellation')
  final bool freeCancellation;
  @JsonKey(name: 'special_offers')
  final bool specialOffers;
  @JsonKey(name: 'eco_certified')
  final bool ecoCertified;

  HotelSearchRequest({
    required this.q,
    required this.checkInDate,
    required this.checkOutDate,
    this.adults = 2,
    this.children = 0,
    this.currency = 'USD',
    this.gl = 'us',
    this.hl = 'en',
    this.sortBy = HotelSortBy.relevance,
    this.minPrice,
    this.maxPrice,
    this.rating,
    this.hotelClass,
    this.propertyTypes,
    this.amenities,
    this.brands,
    this.vacationRentals = false,
    this.bedrooms,
    this.bathrooms,
    this.freeCancellation = false,
    this.specialOffers = false,
    this.ecoCertified = false,
  });

  factory HotelSearchRequest.fromJson(Map<String, dynamic> json) =>
      _$HotelSearchRequestFromJson(json);

  Map<String, dynamic> toJson() => _$HotelSearchRequestToJson(this);
}

@JsonSerializable()
class HotelSearchParams {
  final String? location;
  @JsonKey(name: 'check_in_date')
  final String? checkInDate;
  @JsonKey(name: 'check_out_date')
  final String? checkOutDate;
  final int guests;
  final int rooms;
  @JsonKey(name: 'hotel_class')
  final String? hotelClass;
  final String? amenities;
  @JsonKey(name: 'max_price')
  final int? maxPrice;
  @JsonKey(name: 'vacation_rental')
  final bool vacationRental;

  HotelSearchParams({
    this.location,
    this.checkInDate,
    this.checkOutDate,
    this.guests = 2,
    this.rooms = 1,
    this.hotelClass,
    this.amenities,
    this.maxPrice,
    this.vacationRental = false,
  });

  factory HotelSearchParams.fromJson(Map<String, dynamic> json) =>
      _$HotelSearchParamsFromJson(json);

  Map<String, dynamic> toJson() => _$HotelSearchParamsToJson(this);
}