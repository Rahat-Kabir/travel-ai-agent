// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'chat_models.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

ChatMessage _$ChatMessageFromJson(Map<String, dynamic> json) => ChatMessage(
  role: json['role'] as String,
  content: json['content'] as String,
  timestamp: DateTime.parse(json['timestamp'] as String),
);

Map<String, dynamic> _$ChatMessageToJson(ChatMessage instance) =>
    <String, dynamic>{
      'role': instance.role,
      'content': instance.content,
      'timestamp': instance.timestamp.toIso8601String(),
    };

ChatRequest _$ChatRequestFromJson(Map<String, dynamic> json) => ChatRequest(
  message: json['message'] as String,
  threadId: json['thread_id'] as String?,
);

Map<String, dynamic> _$ChatRequestToJson(ChatRequest instance) =>
    <String, dynamic>{
      'message': instance.message,
      'thread_id': instance.threadId,
    };

ChatResponse _$ChatResponseFromJson(Map<String, dynamic> json) => ChatResponse(
  message: json['message'] as String,
  threadId: json['thread_id'] as String,
  flightResults: json['flight_results'] == null
      ? null
      : FlightSearchResponse.fromJson(
          json['flight_results'] as Map<String, dynamic>,
        ),
  extractedParams: json['extracted_params'] == null
      ? null
      : FlightSearchParams.fromJson(
          json['extracted_params'] as Map<String, dynamic>,
        ),
  needsClarification: json['needs_clarification'] as bool? ?? false,
  missingParams:
      (json['missing_params'] as List<dynamic>?)
          ?.map((e) => e as String)
          .toList() ??
      const [],
);

Map<String, dynamic> _$ChatResponseToJson(ChatResponse instance) =>
    <String, dynamic>{
      'message': instance.message,
      'thread_id': instance.threadId,
      'flight_results': instance.flightResults,
      'extracted_params': instance.extractedParams,
      'needs_clarification': instance.needsClarification,
      'missing_params': instance.missingParams,
    };
