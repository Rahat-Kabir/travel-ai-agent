import 'package:json_annotation/json_annotation.dart';

part 'api_models.g.dart';

enum ResponseStatus {
  @JsonValue('success')
  success,
  @JsonValue('error')
  error,
  @JsonValue('partial')
  partial,
  @JsonValue('pending')
  pending,
}

@JsonSerializable()
class BaseResponse {
  final ResponseStatus status;
  final String? message;
  final DateTime timestamp;
  @JsonKey(name: 'request_id')
  final String? requestId;

  BaseResponse({
    required this.status,
    this.message,
    required this.timestamp,
    this.requestId,
  });

  factory BaseResponse.fromJson(Map<String, dynamic> json) =>
      _$BaseResponseFromJson(json);

  Map<String, dynamic> toJson() => _$BaseResponseToJson(this);
}

@JsonSerializable()
class ErrorResponse extends BaseResponse {
  @JsonKey(name: 'error_code')
  final String? errorCode;
  @JsonKey(name: 'error_details')
  final Map<String, dynamic>? errorDetails;

  ErrorResponse({
    required super.status,
    super.message,
    required super.timestamp,
    super.requestId,
    this.errorCode,
    this.errorDetails,
  });

  factory ErrorResponse.fromJson(Map<String, dynamic> json) =>
      _$ErrorResponseFromJson(json);

  @override
  Map<String, dynamic> toJson() => _$ErrorResponseToJson(this);
}

@JsonSerializable()
class ApiException implements Exception {
  final String message;
  final int? statusCode;
  final String? errorCode;
  final Map<String, dynamic>? details;

  ApiException({
    required this.message,
    this.statusCode,
    this.errorCode,
    this.details,
  });

  factory ApiException.fromJson(Map<String, dynamic> json) =>
      _$ApiExceptionFromJson(json);

  Map<String, dynamic> toJson() => _$ApiExceptionToJson(this);

  @override
  String toString() {
    return 'ApiException: $message (Status: $statusCode, Code: $errorCode)';
  }
}
