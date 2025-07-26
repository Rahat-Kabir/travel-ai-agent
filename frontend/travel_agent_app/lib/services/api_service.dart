import 'dart:convert';
import 'dart:io';
import 'package:http/http.dart' as http;
import '../models/models.dart';

class ApiService {
  static const String _baseUrl = 'http://localhost:8000';
  static const Duration _timeout = Duration(seconds: 30);

  final http.Client _client;

  ApiService({http.Client? client}) : _client = client ?? http.Client();

  /// Send a chat message to the travel agent
  Future<ChatResponse> sendMessage({
    required String message,
    String? threadId,
  }) async {
    try {
      final request = ChatRequest(
        message: message,
        threadId: threadId,
      );

      final response = await _client
          .post(
            Uri.parse('$_baseUrl/chat/message'),
            headers: {
              'Content-Type': 'application/json',
              'Accept': 'application/json',
            },
            body: jsonEncode(request.toJson()),
          )
          .timeout(_timeout);

      return _handleResponse<ChatResponse>(
        response,
        (json) => ChatResponse.fromJson(json),
      );
    } on SocketException {
      throw ApiException(
        message: 'No internet connection. Please check your network.',
        statusCode: 0,
        errorCode: 'NETWORK_ERROR',
      );
    } on HttpException catch (e) {
      throw ApiException(
        message: 'Network error: ${e.message}',
        statusCode: 0,
        errorCode: 'HTTP_ERROR',
      );
    } catch (e) {
      throw ApiException(
        message: 'Failed to send message: ${e.toString()}',
        statusCode: 0,
        errorCode: 'UNKNOWN_ERROR',
      );
    }
  }

  /// Check API health
  Future<Map<String, dynamic>> checkHealth() async {
    try {
      final response = await _client
          .get(
            Uri.parse('$_baseUrl/health'),
            headers: {
              'Accept': 'application/json',
            },
          )
          .timeout(_timeout);

      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      } else {
        throw ApiException(
          message: 'Health check failed',
          statusCode: response.statusCode,
          errorCode: 'HEALTH_CHECK_FAILED',
        );
      }
    } on SocketException {
      throw ApiException(
        message: 'Cannot connect to server. Please check if the backend is running.',
        statusCode: 0,
        errorCode: 'CONNECTION_ERROR',
      );
    } catch (e) {
      throw ApiException(
        message: 'Health check failed: ${e.toString()}',
        statusCode: 0,
        errorCode: 'HEALTH_CHECK_ERROR',
      );
    }
  }

  /// Generic response handler
  T _handleResponse<T>(
    http.Response response,
    T Function(Map<String, dynamic>) fromJson,
  ) {
    final statusCode = response.statusCode;
    
    if (statusCode >= 200 && statusCode < 300) {
      try {
        final Map<String, dynamic> json = jsonDecode(response.body);
        return fromJson(json);
      } catch (e) {
        throw ApiException(
          message: 'Failed to parse response: ${e.toString()}',
          statusCode: statusCode,
          errorCode: 'PARSE_ERROR',
        );
      }
    } else {
      // Try to parse error response
      try {
        final Map<String, dynamic> errorJson = jsonDecode(response.body);
        final errorResponse = ErrorResponse.fromJson(errorJson);
        
        throw ApiException(
          message: errorResponse.message ?? 'Unknown error occurred',
          statusCode: statusCode,
          errorCode: errorResponse.errorCode,
          details: errorResponse.errorDetails,
        );
      } catch (e) {
        // If we can't parse the error response, create a generic error
        throw ApiException(
          message: 'Request failed with status $statusCode',
          statusCode: statusCode,
          errorCode: 'HTTP_ERROR',
        );
      }
    }
  }

  /// Dispose of the HTTP client
  void dispose() {
    _client.close();
  }
}
