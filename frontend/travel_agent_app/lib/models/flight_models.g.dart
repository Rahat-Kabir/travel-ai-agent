// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'flight_models.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

Airport _$AirportFromJson(Map<String, dynamic> json) => Airport(
  id: json['id'] as String,
  name: json['name'] as String,
  city: json['city'] as String,
  country: json['country'] as String,
);

Map<String, dynamic> _$AirportToJson(Airport instance) => <String, dynamic>{
  'id': instance.id,
  'name': instance.name,
  'city': instance.city,
  'country': instance.country,
};

Flight _$FlightFromJson(Map<String, dynamic> json) => Flight(
  flightNumber: json['flight_number'] as String,
  airline: json['airline'] as String,
  departureAirport: Airport.fromJson(
    json['departure_airport'] as Map<String, dynamic>,
  ),
  arrivalAirport: Airport.fromJson(
    json['arrival_airport'] as Map<String, dynamic>,
  ),
  departureTime: DateTime.parse(json['departure_time'] as String),
  arrivalTime: DateTime.parse(json['arrival_time'] as String),
  duration: (json['duration'] as num).toInt(),
  aircraft: json['aircraft'] as String,
  travelClass: $enumDecode(_$TravelClassEnumMap, json['travel_class']),
);

Map<String, dynamic> _$FlightToJson(Flight instance) => <String, dynamic>{
  'flight_number': instance.flightNumber,
  'airline': instance.airline,
  'departure_airport': instance.departureAirport,
  'arrival_airport': instance.arrivalAirport,
  'departure_time': instance.departureTime.toIso8601String(),
  'arrival_time': instance.arrivalTime.toIso8601String(),
  'duration': instance.duration,
  'aircraft': instance.aircraft,
  'travel_class': _$TravelClassEnumMap[instance.travelClass]!,
};

const _$TravelClassEnumMap = {
  TravelClass.economy: 'economy',
  TravelClass.premiumEconomy: 'premium_economy',
  TravelClass.business: 'business',
  TravelClass.first: 'first',
};

Layover _$LayoverFromJson(Map<String, dynamic> json) => Layover(
  airport: Airport.fromJson(json['airport'] as Map<String, dynamic>),
  duration: (json['duration'] as num).toInt(),
);

Map<String, dynamic> _$LayoverToJson(Layover instance) => <String, dynamic>{
  'airport': instance.airport,
  'duration': instance.duration,
};

CarbonEmissions _$CarbonEmissionsFromJson(Map<String, dynamic> json) =>
    CarbonEmissions(
      thisFlight: (json['this_flight'] as num).toInt(),
      typicalForThisRoute: (json['typical_for_this_route'] as num).toInt(),
      differencePercent: (json['difference_percent'] as num).toInt(),
    );

Map<String, dynamic> _$CarbonEmissionsToJson(CarbonEmissions instance) =>
    <String, dynamic>{
      'this_flight': instance.thisFlight,
      'typical_for_this_route': instance.typicalForThisRoute,
      'difference_percent': instance.differencePercent,
    };

FlightOption _$FlightOptionFromJson(Map<String, dynamic> json) => FlightOption(
  flights: (json['flights'] as List<dynamic>)
      .map((e) => Flight.fromJson(e as Map<String, dynamic>))
      .toList(),
  layovers: (json['layovers'] as List<dynamic>)
      .map((e) => Layover.fromJson(e as Map<String, dynamic>))
      .toList(),
  totalDuration: (json['total_duration'] as num).toInt(),
  price: (json['price'] as num).toDouble(),
  currency: json['currency'] as String,
  carbonEmissions: json['carbon_emissions'] == null
      ? null
      : CarbonEmissions.fromJson(
          json['carbon_emissions'] as Map<String, dynamic>,
        ),
  bookingToken: json['booking_token'] as String?,
);

Map<String, dynamic> _$FlightOptionToJson(FlightOption instance) =>
    <String, dynamic>{
      'flights': instance.flights,
      'layovers': instance.layovers,
      'total_duration': instance.totalDuration,
      'price': instance.price,
      'currency': instance.currency,
      'carbon_emissions': instance.carbonEmissions,
      'booking_token': instance.bookingToken,
    };

PriceInsights _$PriceInsightsFromJson(Map<String, dynamic> json) =>
    PriceInsights(
      lowestPrice: (json['lowest_price'] as num?)?.toDouble(),
      priceLevel: json['price_level'] as String?,
      typicalPriceRange: (json['typical_price_range'] as List<dynamic>?)
          ?.map((e) => (e as num).toDouble())
          .toList(),
      priceHistory: (json['price_history'] as List<dynamic>?)
          ?.map((e) => (e as num).toDouble())
          .toList(),
    );

Map<String, dynamic> _$PriceInsightsToJson(PriceInsights instance) =>
    <String, dynamic>{
      'lowest_price': instance.lowestPrice,
      'price_level': instance.priceLevel,
      'typical_price_range': instance.typicalPriceRange,
      'price_history': instance.priceHistory,
    };

FlightSearchResponse _$FlightSearchResponseFromJson(
  Map<String, dynamic> json,
) => FlightSearchResponse(
  searchId: json['search_id'] as String,
  searchParams: json['search_params'] as Map<String, dynamic>,
  flights: (json['flights'] as List<dynamic>)
      .map((e) => FlightOption.fromJson(e as Map<String, dynamic>))
      .toList(),
  priceInsights: json['price_insights'] == null
      ? null
      : PriceInsights.fromJson(json['price_insights'] as Map<String, dynamic>),
  searchMetadata: json['search_metadata'] as Map<String, dynamic>?,
);

Map<String, dynamic> _$FlightSearchResponseToJson(
  FlightSearchResponse instance,
) => <String, dynamic>{
  'search_id': instance.searchId,
  'search_params': instance.searchParams,
  'flights': instance.flights,
  'price_insights': instance.priceInsights,
  'search_metadata': instance.searchMetadata,
};

FlightSearchParams _$FlightSearchParamsFromJson(Map<String, dynamic> json) =>
    FlightSearchParams(
      departureLocation: json['departure_location'] as String?,
      arrivalLocation: json['arrival_location'] as String?,
      departureDate: json['departure_date'] as String?,
      returnDate: json['return_date'] as String?,
      passengers: (json['passengers'] as num?)?.toInt(),
      tripType: $enumDecodeNullable(_$TripTypeEnumMap, json['trip_type']),
      travelClass: $enumDecodeNullable(
        _$TravelClassEnumMap,
        json['travel_class'],
      ),
    );

Map<String, dynamic> _$FlightSearchParamsToJson(FlightSearchParams instance) =>
    <String, dynamic>{
      'departure_location': instance.departureLocation,
      'arrival_location': instance.arrivalLocation,
      'departure_date': instance.departureDate,
      'return_date': instance.returnDate,
      'passengers': instance.passengers,
      'trip_type': _$TripTypeEnumMap[instance.tripType],
      'travel_class': _$TravelClassEnumMap[instance.travelClass],
    };

const _$TripTypeEnumMap = {
  TripType.roundTrip: 'round_trip',
  TripType.oneWay: 'one_way',
  TripType.multiCity: 'multi_city',
};
