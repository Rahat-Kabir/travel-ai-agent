import 'package:json_annotation/json_annotation.dart';

part 'flight_models.g.dart';

enum TripType {
  @JsonValue('round_trip')
  roundTrip,
  @JsonValue('one_way')
  oneWay,
  @JsonValue('multi_city')
  multiCity,
}

enum TravelClass {
  @JsonValue('economy')
  economy,
  @JsonValue('premium_economy')
  premiumEconomy,
  @JsonValue('business')
  business,
  @JsonValue('first')
  first,
}

enum SortBy {
  @JsonValue('best')
  best,
  @JsonValue('price')
  price,
  @JsonValue('duration')
  duration,
  @JsonValue('departure_time')
  departureTime,
  @JsonValue('arrival_time')
  arrivalTime,
}

enum Stops {
  @JsonValue('any')
  any,
  @JsonValue('nonstop')
  nonstop,
  @JsonValue('one_stop')
  oneStop,
  @JsonValue('two_stops')
  twoStops,
}

@JsonSerializable()
class Airport {
  final String id;
  final String name;
  final String city;
  final String country;

  Airport({
    required this.id,
    required this.name,
    required this.city,
    required this.country,
  });

  factory Airport.fromJson(Map<String, dynamic> json) =>
      _$AirportFromJson(json);

  Map<String, dynamic> toJson() => _$AirportToJson(this);
}

@JsonSerializable()
class Flight {
  @JsonKey(name: 'flight_number')
  final String flightNumber;
  final String airline;
  @JsonKey(name: 'departure_airport')
  final Airport departureAirport;
  @JsonKey(name: 'arrival_airport')
  final Airport arrivalAirport;
  @JsonKey(name: 'departure_time')
  final DateTime departureTime;
  @JsonKey(name: 'arrival_time')
  final DateTime arrivalTime;
  final int duration;
  final String aircraft;
  @JsonKey(name: 'travel_class')
  final TravelClass travelClass;

  Flight({
    required this.flightNumber,
    required this.airline,
    required this.departureAirport,
    required this.arrivalAirport,
    required this.departureTime,
    required this.arrivalTime,
    required this.duration,
    required this.aircraft,
    required this.travelClass,
  });

  factory Flight.fromJson(Map<String, dynamic> json) =>
      _$FlightFromJson(json);

  Map<String, dynamic> toJson() => _$FlightToJson(this);
}

@JsonSerializable()
class Layover {
  final Airport airport;
  final int duration;

  Layover({
    required this.airport,
    required this.duration,
  });

  factory Layover.fromJson(Map<String, dynamic> json) =>
      _$LayoverFromJson(json);

  Map<String, dynamic> toJson() => _$LayoverToJson(this);
}

@JsonSerializable()
class CarbonEmissions {
  @JsonKey(name: 'this_flight')
  final int thisFlight;
  @JsonKey(name: 'typical_for_this_route')
  final int typicalForThisRoute;
  @JsonKey(name: 'difference_percent')
  final int differencePercent;

  CarbonEmissions({
    required this.thisFlight,
    required this.typicalForThisRoute,
    required this.differencePercent,
  });

  factory CarbonEmissions.fromJson(Map<String, dynamic> json) =>
      _$CarbonEmissionsFromJson(json);

  Map<String, dynamic> toJson() => _$CarbonEmissionsToJson(this);
}

@JsonSerializable()
class FlightOption {
  final List<Flight> flights;
  final List<Layover> layovers;
  @JsonKey(name: 'total_duration')
  final int totalDuration;
  final double price;
  final String currency;
  @JsonKey(name: 'carbon_emissions')
  final CarbonEmissions? carbonEmissions;
  @JsonKey(name: 'booking_token')
  final String? bookingToken;

  FlightOption({
    required this.flights,
    required this.layovers,
    required this.totalDuration,
    required this.price,
    required this.currency,
    this.carbonEmissions,
    this.bookingToken,
  });

  factory FlightOption.fromJson(Map<String, dynamic> json) =>
      _$FlightOptionFromJson(json);

  Map<String, dynamic> toJson() => _$FlightOptionToJson(this);
}

@JsonSerializable()
class PriceInsights {
  @JsonKey(name: 'lowest_price')
  final double? lowestPrice;
  @JsonKey(name: 'price_level')
  final String? priceLevel;
  @JsonKey(name: 'typical_price_range')
  final List<double>? typicalPriceRange;
  @JsonKey(name: 'price_history')
  final List<double>? priceHistory;

  PriceInsights({
    this.lowestPrice,
    this.priceLevel,
    this.typicalPriceRange,
    this.priceHistory,
  });

  factory PriceInsights.fromJson(Map<String, dynamic> json) =>
      _$PriceInsightsFromJson(json);

  Map<String, dynamic> toJson() => _$PriceInsightsToJson(this);
}

@JsonSerializable()
class FlightSearchResponse {
  @JsonKey(name: 'search_id')
  final String searchId;
  @JsonKey(name: 'search_params')
  final Map<String, dynamic> searchParams;
  final List<FlightOption> flights;
  @JsonKey(name: 'price_insights')
  final PriceInsights? priceInsights;
  @JsonKey(name: 'search_metadata')
  final Map<String, dynamic>? searchMetadata;

  FlightSearchResponse({
    required this.searchId,
    required this.searchParams,
    required this.flights,
    this.priceInsights,
    this.searchMetadata,
  });

  factory FlightSearchResponse.fromJson(Map<String, dynamic> json) =>
      _$FlightSearchResponseFromJson(json);

  Map<String, dynamic> toJson() => _$FlightSearchResponseToJson(this);
}

@JsonSerializable()
class FlightSearchParams {
  @JsonKey(name: 'departure_location')
  final String? departureLocation;
  @JsonKey(name: 'arrival_location')
  final String? arrivalLocation;
  @JsonKey(name: 'departure_date')
  final String? departureDate;
  @JsonKey(name: 'return_date')
  final String? returnDate;
  final int? passengers;
  @JsonKey(name: 'trip_type')
  final TripType? tripType;
  @JsonKey(name: 'travel_class')
  final TravelClass? travelClass;

  FlightSearchParams({
    this.departureLocation,
    this.arrivalLocation,
    this.departureDate,
    this.returnDate,
    this.passengers,
    this.tripType,
    this.travelClass,
  });

  factory FlightSearchParams.fromJson(Map<String, dynamic> json) =>
      _$FlightSearchParamsFromJson(json);

  Map<String, dynamic> toJson() => _$FlightSearchParamsToJson(this);
}
