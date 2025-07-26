import 'package:json_annotation/json_annotation.dart';
import 'flight_models.dart';

part 'chat_models.g.dart';

@JsonSerializable()
class ChatMessage {
  final String role;
  final String content;
  final DateTime timestamp;

  ChatMessage({
    required this.role,
    required this.content,
    required this.timestamp,
  });

  factory ChatMessage.fromJson(Map<String, dynamic> json) =>
      _$ChatMessageFromJson(json);

  Map<String, dynamic> toJson() => _$ChatMessageToJson(this);

  // Helper constructors
  ChatMessage.user(String content)
      : role = 'user',
        content = content,
        timestamp = DateTime.now();

  ChatMessage.assistant(String content)
      : role = 'assistant',
        content = content,
        timestamp = DateTime.now();

  bool get isUser => role == 'user';
  bool get isAssistant => role == 'assistant';
}

@JsonSerializable()
class ChatRequest {
  final String message;
  @JsonKey(name: 'thread_id')
  final String? threadId;

  ChatRequest({
    required this.message,
    this.threadId,
  });

  factory ChatRequest.fromJson(Map<String, dynamic> json) =>
      _$ChatRequestFromJson(json);

  Map<String, dynamic> toJson() => _$ChatRequestToJson(this);
}

@JsonSerializable()
class ChatResponse {
  final String message;
  @JsonKey(name: 'thread_id')
  final String threadId;
  @JsonKey(name: 'flight_results')
  final FlightSearchResponse? flightResults;
  @JsonKey(name: 'extracted_params')
  final FlightSearchParams? extractedParams;
  @JsonKey(name: 'needs_clarification')
  final bool needsClarification;
  @JsonKey(name: 'missing_params')
  final List<String> missingParams;

  ChatResponse({
    required this.message,
    required this.threadId,
    this.flightResults,
    this.extractedParams,
    this.needsClarification = false,
    this.missingParams = const [],
  });

  factory ChatResponse.fromJson(Map<String, dynamic> json) =>
      _$ChatResponseFromJson(json);

  Map<String, dynamic> toJson() => _$ChatResponseToJson(this);
}
