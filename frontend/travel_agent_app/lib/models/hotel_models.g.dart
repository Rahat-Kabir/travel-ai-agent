// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'hotel_models.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

GPSCoordinates _$GPSCoordinatesFromJson(Map<String, dynamic> json) =>
    GPSCoordinates(
      latitude: (json['latitude'] as num).toDouble(),
      longitude: (json['longitude'] as num).toDouble(),
    );

Map<String, dynamic> _$GPSCoordinatesToJson(GPSCoordinates instance) =>
    <String, dynamic>{
      'latitude': instance.latitude,
      'longitude': instance.longitude,
    };

Transportation _$TransportationFromJson(Map<String, dynamic> json) =>
    Transportation(
      type: json['type'] as String,
      duration: json['duration'] as String,
    );

Map<String, dynamic> _$TransportationToJson(Transportation instance) =>
    <String, dynamic>{'type': instance.type, 'duration': instance.duration};

NearbyPlace _$NearbyPlaceFromJson(Map<String, dynamic> json) => NearbyPlace(
  name: json['name'] as String,
  transportations:
      (json['transportations'] as List<dynamic>?)
          ?.map((e) => Transportation.fromJson(e as Map<String, dynamic>))
          .toList() ??
      const [],
);

Map<String, dynamic> _$NearbyPlaceToJson(NearbyPlace instance) =>
    <String, dynamic>{
      'name': instance.name,
      'transportations': instance.transportations,
    };

HotelImage _$HotelImageFromJson(Map<String, dynamic> json) => HotelImage(
  thumbnail: json['thumbnail'] as String,
  originalImage: json['original_image'] as String,
);

Map<String, dynamic> _$HotelImageToJson(HotelImage instance) =>
    <String, dynamic>{
      'thumbnail': instance.thumbnail,
      'original_image': instance.originalImage,
    };

RateInfo _$RateInfoFromJson(Map<String, dynamic> json) => RateInfo(
  lowest: json['lowest'] as String?,
  extractedLowest: (json['extracted_lowest'] as num?)?.toDouble(),
  beforeTaxesFees: json['before_taxes_fees'] as String?,
  extractedBeforeTaxesFees: (json['extracted_before_taxes_fees'] as num?)
      ?.toDouble(),
);

Map<String, dynamic> _$RateInfoToJson(RateInfo instance) => <String, dynamic>{
  'lowest': instance.lowest,
  'extracted_lowest': instance.extractedLowest,
  'before_taxes_fees': instance.beforeTaxesFees,
  'extracted_before_taxes_fees': instance.extractedBeforeTaxesFees,
};

PriceSource _$PriceSourceFromJson(Map<String, dynamic> json) => PriceSource(
  source: json['source'] as String,
  logo: json['logo'] as String?,
  numGuests: (json['num_guests'] as num?)?.toInt(),
  ratePerNight: json['rate_per_night'] == null
      ? null
      : RateInfo.fromJson(json['rate_per_night'] as Map<String, dynamic>),
);

Map<String, dynamic> _$PriceSourceToJson(PriceSource instance) =>
    <String, dynamic>{
      'source': instance.source,
      'logo': instance.logo,
      'num_guests': instance.numGuests,
      'rate_per_night': instance.ratePerNight,
    };

RatingBreakdown _$RatingBreakdownFromJson(Map<String, dynamic> json) =>
    RatingBreakdown(
      name: json['name'] as String,
      description: json['description'] as String?,
      totalMentioned: (json['total_mentioned'] as num?)?.toInt(),
      positive: (json['positive'] as num?)?.toInt(),
      negative: (json['negative'] as num?)?.toInt(),
      neutral: (json['neutral'] as num?)?.toInt(),
    );

Map<String, dynamic> _$RatingBreakdownToJson(RatingBreakdown instance) =>
    <String, dynamic>{
      'name': instance.name,
      'description': instance.description,
      'total_mentioned': instance.totalMentioned,
      'positive': instance.positive,
      'negative': instance.negative,
      'neutral': instance.neutral,
    };

StarRating _$StarRatingFromJson(Map<String, dynamic> json) => StarRating(
  stars: (json['stars'] as num).toInt(),
  count: (json['count'] as num).toInt(),
);

Map<String, dynamic> _$StarRatingToJson(StarRating instance) =>
    <String, dynamic>{'stars': instance.stars, 'count': instance.count};

HotelProperty _$HotelPropertyFromJson(
  Map<String, dynamic> json,
) => HotelProperty(
  type: json['type'] as String,
  name: json['name'] as String,
  description: json['description'] as String?,
  link: json['link'] as String?,
  logo: json['logo'] as String?,
  sponsored: json['sponsored'] as bool? ?? false,
  ecoCertified: json['eco_certified'] as bool? ?? false,
  gpsCoordinates: json['gps_coordinates'] == null
      ? null
      : GPSCoordinates.fromJson(
          json['gps_coordinates'] as Map<String, dynamic>,
        ),
  nearbyPlaces:
      (json['nearby_places'] as List<dynamic>?)
          ?.map((e) => NearbyPlace.fromJson(e as Map<String, dynamic>))
          .toList() ??
      const [],
  checkInTime: json['check_in_time'] as String?,
  checkOutTime: json['check_out_time'] as String?,
  ratePerNight: json['rate_per_night'] == null
      ? null
      : RateInfo.fromJson(json['rate_per_night'] as Map<String, dynamic>),
  totalRate: json['total_rate'] == null
      ? null
      : RateInfo.fromJson(json['total_rate'] as Map<String, dynamic>),
  prices:
      (json['prices'] as List<dynamic>?)
          ?.map((e) => PriceSource.fromJson(e as Map<String, dynamic>))
          .toList() ??
      const [],
  hotelClass: json['hotel_class'] as String?,
  extractedHotelClass: (json['extracted_hotel_class'] as num?)?.toInt(),
  images:
      (json['images'] as List<dynamic>?)
          ?.map((e) => HotelImage.fromJson(e as Map<String, dynamic>))
          .toList() ??
      const [],
  overallRating: (json['overall_rating'] as num?)?.toDouble(),
  reviews: (json['reviews'] as num?)?.toInt(),
  ratings:
      (json['ratings'] as List<dynamic>?)
          ?.map((e) => StarRating.fromJson(e as Map<String, dynamic>))
          .toList() ??
      const [],
  locationRating: (json['location_rating'] as num?)?.toDouble(),
  reviewsBreakdown:
      (json['reviews_breakdown'] as List<dynamic>?)
          ?.map((e) => RatingBreakdown.fromJson(e as Map<String, dynamic>))
          .toList() ??
      const [],
  amenities:
      (json['amenities'] as List<dynamic>?)?.map((e) => e as String).toList() ??
      const [],
  excludedAmenities:
      (json['excluded_amenities'] as List<dynamic>?)
          ?.map((e) => e as String)
          .toList() ??
      const [],
  essentialInfo:
      (json['essential_info'] as List<dynamic>?)
          ?.map((e) => e as String)
          .toList() ??
      const [],
  propertyToken: json['property_token'] as String?,
  serpapiPropertyDetailsLink: json['serpapi_property_details_link'] as String?,
);

Map<String, dynamic> _$HotelPropertyToJson(HotelProperty instance) =>
    <String, dynamic>{
      'type': instance.type,
      'name': instance.name,
      'description': instance.description,
      'link': instance.link,
      'logo': instance.logo,
      'sponsored': instance.sponsored,
      'eco_certified': instance.ecoCertified,
      'gps_coordinates': instance.gpsCoordinates,
      'nearby_places': instance.nearbyPlaces,
      'check_in_time': instance.checkInTime,
      'check_out_time': instance.checkOutTime,
      'rate_per_night': instance.ratePerNight,
      'total_rate': instance.totalRate,
      'prices': instance.prices,
      'hotel_class': instance.hotelClass,
      'extracted_hotel_class': instance.extractedHotelClass,
      'images': instance.images,
      'overall_rating': instance.overallRating,
      'reviews': instance.reviews,
      'ratings': instance.ratings,
      'location_rating': instance.locationRating,
      'reviews_breakdown': instance.reviewsBreakdown,
      'amenities': instance.amenities,
      'excluded_amenities': instance.excludedAmenities,
      'essential_info': instance.essentialInfo,
      'property_token': instance.propertyToken,
      'serpapi_property_details_link': instance.serpapiPropertyDetailsLink,
    };

HotelAd _$HotelAdFromJson(Map<String, dynamic> json) => HotelAd(
  name: json['name'] as String,
  source: json['source'] as String,
  sourceIcon: json['source_icon'] as String?,
  link: json['link'] as String,
  propertyToken: json['property_token'] as String?,
  serpapiPropertyDetailsLink: json['serpapi_property_details_link'] as String?,
  gpsCoordinates: json['gps_coordinates'] == null
      ? null
      : GPSCoordinates.fromJson(
          json['gps_coordinates'] as Map<String, dynamic>,
        ),
  hotelClass: (json['hotel_class'] as num?)?.toInt(),
  thumbnail: json['thumbnail'] as String?,
  overallRating: (json['overall_rating'] as num?)?.toDouble(),
  reviews: (json['reviews'] as num?)?.toInt(),
  price: json['price'] as String?,
  extractedPrice: (json['extracted_price'] as num?)?.toDouble(),
  amenities:
      (json['amenities'] as List<dynamic>?)?.map((e) => e as String).toList() ??
      const [],
  freeCancellation: json['free_cancellation'] as bool? ?? false,
);

Map<String, dynamic> _$HotelAdToJson(HotelAd instance) => <String, dynamic>{
  'name': instance.name,
  'source': instance.source,
  'source_icon': instance.sourceIcon,
  'link': instance.link,
  'property_token': instance.propertyToken,
  'serpapi_property_details_link': instance.serpapiPropertyDetailsLink,
  'gps_coordinates': instance.gpsCoordinates,
  'hotel_class': instance.hotelClass,
  'thumbnail': instance.thumbnail,
  'overall_rating': instance.overallRating,
  'reviews': instance.reviews,
  'price': instance.price,
  'extracted_price': instance.extractedPrice,
  'amenities': instance.amenities,
  'free_cancellation': instance.freeCancellation,
};

HotelBrand _$HotelBrandFromJson(Map<String, dynamic> json) => HotelBrand(
  id: (json['id'] as num).toInt(),
  name: json['name'] as String,
  children: (json['children'] as List<dynamic>?)
      ?.map((e) => HotelBrand.fromJson(e as Map<String, dynamic>))
      .toList(),
);

Map<String, dynamic> _$HotelBrandToJson(HotelBrand instance) =>
    <String, dynamic>{
      'id': instance.id,
      'name': instance.name,
      'children': instance.children,
    };

HotelSearchResponse _$HotelSearchResponseFromJson(Map<String, dynamic> json) =>
    HotelSearchResponse(
      properties:
          (json['properties'] as List<dynamic>?)
              ?.map((e) => HotelProperty.fromJson(e as Map<String, dynamic>))
              .toList() ??
          const [],
      ads:
          (json['ads'] as List<dynamic>?)
              ?.map((e) => HotelAd.fromJson(e as Map<String, dynamic>))
              .toList() ??
          const [],
      brands:
          (json['brands'] as List<dynamic>?)
              ?.map((e) => HotelBrand.fromJson(e as Map<String, dynamic>))
              .toList() ??
          const [],
      searchMetadata:
          json['search_metadata'] as Map<String, dynamic>? ?? const {},
      searchInformation:
          json['search_information'] as Map<String, dynamic>? ?? const {},
      serpapiPagination: json['serpapi_pagination'] as Map<String, dynamic>?,
      error: json['error'] as String?,
    );

Map<String, dynamic> _$HotelSearchResponseToJson(
  HotelSearchResponse instance,
) => <String, dynamic>{
  'properties': instance.properties,
  'ads': instance.ads,
  'brands': instance.brands,
  'search_metadata': instance.searchMetadata,
  'search_information': instance.searchInformation,
  'serpapi_pagination': instance.serpapiPagination,
  'error': instance.error,
};

HotelSearchRequest _$HotelSearchRequestFromJson(Map<String, dynamic> json) =>
    HotelSearchRequest(
      q: json['q'] as String,
      checkInDate: json['check_in_date'] as String,
      checkOutDate: json['check_out_date'] as String,
      adults: (json['adults'] as num?)?.toInt() ?? 2,
      children: (json['children'] as num?)?.toInt() ?? 0,
      currency: json['currency'] as String? ?? 'USD',
      gl: json['gl'] as String? ?? 'us',
      hl: json['hl'] as String? ?? 'en',
      sortBy:
          $enumDecodeNullable(_$HotelSortByEnumMap, json['sort_by']) ??
          HotelSortBy.relevance,
      minPrice: (json['min_price'] as num?)?.toInt(),
      maxPrice: (json['max_price'] as num?)?.toInt(),
      rating: $enumDecodeNullable(_$HotelRatingEnumMap, json['rating']),
      hotelClass: json['hotel_class'] as String?,
      propertyTypes: json['property_types'] as String?,
      amenities: json['amenities'] as String?,
      brands: json['brands'] as String?,
      vacationRentals: json['vacation_rentals'] as bool? ?? false,
      bedrooms: (json['bedrooms'] as num?)?.toInt(),
      bathrooms: (json['bathrooms'] as num?)?.toInt(),
      freeCancellation: json['free_cancellation'] as bool? ?? false,
      specialOffers: json['special_offers'] as bool? ?? false,
      ecoCertified: json['eco_certified'] as bool? ?? false,
    );

Map<String, dynamic> _$HotelSearchRequestToJson(HotelSearchRequest instance) =>
    <String, dynamic>{
      'q': instance.q,
      'check_in_date': instance.checkInDate,
      'check_out_date': instance.checkOutDate,
      'adults': instance.adults,
      'children': instance.children,
      'currency': instance.currency,
      'gl': instance.gl,
      'hl': instance.hl,
      'sort_by': _$HotelSortByEnumMap[instance.sortBy]!,
      'min_price': instance.minPrice,
      'max_price': instance.maxPrice,
      'rating': _$HotelRatingEnumMap[instance.rating],
      'hotel_class': instance.hotelClass,
      'property_types': instance.propertyTypes,
      'amenities': instance.amenities,
      'brands': instance.brands,
      'vacation_rentals': instance.vacationRentals,
      'bedrooms': instance.bedrooms,
      'bathrooms': instance.bathrooms,
      'free_cancellation': instance.freeCancellation,
      'special_offers': instance.specialOffers,
      'eco_certified': instance.ecoCertified,
    };

const _$HotelSortByEnumMap = {
  HotelSortBy.relevance: '0',
  HotelSortBy.lowestPrice: '3',
  HotelSortBy.highestRating: '8',
  HotelSortBy.mostReviewed: '13',
};

const _$HotelRatingEnumMap = {
  HotelRating.threeFivePlus: '7',
  HotelRating.fourPlus: '8',
  HotelRating.fourFivePlus: '9',
};

HotelSearchParams _$HotelSearchParamsFromJson(Map<String, dynamic> json) =>
    HotelSearchParams(
      location: json['location'] as String?,
      checkInDate: json['check_in_date'] as String?,
      checkOutDate: json['check_out_date'] as String?,
      guests: (json['guests'] as num?)?.toInt() ?? 2,
      rooms: (json['rooms'] as num?)?.toInt() ?? 1,
      hotelClass: json['hotel_class'] as String?,
      amenities: json['amenities'] as String?,
      maxPrice: (json['max_price'] as num?)?.toInt(),
      vacationRental: json['vacation_rental'] as bool? ?? false,
    );

Map<String, dynamic> _$HotelSearchParamsToJson(HotelSearchParams instance) =>
    <String, dynamic>{
      'location': instance.location,
      'check_in_date': instance.checkInDate,
      'check_out_date': instance.checkOutDate,
      'guests': instance.guests,
      'rooms': instance.rooms,
      'hotel_class': instance.hotelClass,
      'amenities': instance.amenities,
      'max_price': instance.maxPrice,
      'vacation_rental': instance.vacationRental,
    };
