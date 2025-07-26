// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'api_models.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

BaseResponse _$BaseResponseFromJson(Map<String, dynamic> json) => BaseResponse(
  status: $enumDecode(_$ResponseStatusEnumMap, json['status']),
  message: json['message'] as String?,
  timestamp: DateTime.parse(json['timestamp'] as String),
  requestId: json['request_id'] as String?,
);

Map<String, dynamic> _$BaseResponseToJson(BaseResponse instance) =>
    <String, dynamic>{
      'status': _$ResponseStatusEnumMap[instance.status]!,
      'message': instance.message,
      'timestamp': instance.timestamp.toIso8601String(),
      'request_id': instance.requestId,
    };

const _$ResponseStatusEnumMap = {
  ResponseStatus.success: 'success',
  ResponseStatus.error: 'error',
  ResponseStatus.partial: 'partial',
  ResponseStatus.pending: 'pending',
};

ErrorResponse _$ErrorResponseFromJson(Map<String, dynamic> json) =>
    ErrorResponse(
      status: $enumDecode(_$ResponseStatusEnumMap, json['status']),
      message: json['message'] as String?,
      timestamp: DateTime.parse(json['timestamp'] as String),
      requestId: json['request_id'] as String?,
      errorCode: json['error_code'] as String?,
      errorDetails: json['error_details'] as Map<String, dynamic>?,
    );

Map<String, dynamic> _$ErrorResponseToJson(ErrorResponse instance) =>
    <String, dynamic>{
      'status': _$ResponseStatusEnumMap[instance.status]!,
      'message': instance.message,
      'timestamp': instance.timestamp.toIso8601String(),
      'request_id': instance.requestId,
      'error_code': instance.errorCode,
      'error_details': instance.errorDetails,
    };

ApiException _$ApiExceptionFromJson(Map<String, dynamic> json) => ApiException(
  message: json['message'] as String,
  statusCode: (json['statusCode'] as num?)?.toInt(),
  errorCode: json['errorCode'] as String?,
  details: json['details'] as Map<String, dynamic>?,
);

Map<String, dynamic> _$ApiExceptionToJson(ApiException instance) =>
    <String, dynamic>{
      'message': instance.message,
      'statusCode': instance.statusCode,
      'errorCode': instance.errorCode,
      'details': instance.details,
    };
