import 'package:flutter/foundation.dart';
import 'package:uuid/uuid.dart';
import '../models/models.dart';
import '../services/api_service.dart';

class ChatProvider extends ChangeNotifier {
  final ApiService _apiService = ApiService();
  final List<ChatMessage> _messages = [];
  bool _isLoading = false;
  bool _isConnected = true;
  String? _currentThreadId;
  FlightSearchResponse? _lastFlightResults;
  HotelSearchResponse? _lastHotelResults;
  String? _lastError;

  // Getters
  List<ChatMessage> get messages => List.unmodifiable(_messages);
  bool get isLoading => _isLoading;
  bool get isConnected => _isConnected;
  String? get currentThreadId => _currentThreadId;
  FlightSearchResponse? get lastFlightResults => _lastFlightResults;
  HotelSearchResponse? get lastHotelResults => _lastHotelResults;
  String? get lastError => _lastError;

  // Initialize thread ID
  ChatProvider() {
    _currentThreadId = const Uuid().v4();
    _checkConnection();
  }

  /// Check API connection status
  Future<void> _checkConnection() async {
    try {
      await _apiService.checkHealth();
      _isConnected = true;
    } catch (e) {
      _isConnected = false;
      debugPrint('API connection failed: $e');
    }
    notifyListeners();
  }

  /// Add a message to the chat
  void addMessage(ChatMessage message) {
    _messages.add(message);
    notifyListeners();
  }

  /// Send a message to the API
  Future<void> sendMessage(String messageText) async {
    if (messageText.trim().isEmpty) return;

    _setLoading(true);
    _lastError = null;

    try {
      final response = await _apiService.sendMessage(
        message: messageText,
        threadId: _currentThreadId,
      );

      // Update thread ID if it changed
      if (response.threadId != _currentThreadId) {
        _currentThreadId = response.threadId;
      }

      // Add assistant response
      addMessage(ChatMessage.assistant(response.message));

      // Store flight results if available
      if (response.flightResults != null) {
        _lastFlightResults = response.flightResults;
      }

      // Store hotel results if available
      if (response.hotelResults != null) {
        _lastHotelResults = response.hotelResults;
      }

      // Update connection status
      _isConnected = true;

    } on ApiException catch (e) {
      _handleApiError(e);
    } catch (e) {
      _handleGenericError(e);
    } finally {
      _setLoading(false);
    }
  }

  /// Handle API-specific errors
  void _handleApiError(ApiException error) {
    _lastError = error.message;
    
    String errorMessage;
    switch (error.errorCode) {
      case 'NETWORK_ERROR':
      case 'CONNECTION_ERROR':
        _isConnected = false;
        errorMessage = 'Connection lost. Please check your internet connection.';
        break;
      case 'TIMEOUT_ERROR':
        errorMessage = 'Request timed out. Please try again.';
        break;
      case 'PARSE_ERROR':
        errorMessage = 'Received invalid response from server.';
        break;
      default:
        errorMessage = error.message;
    }

    addMessage(ChatMessage.assistant(
      'Sorry, I encountered an error: $errorMessage'
    ));

    debugPrint('API Error: ${error.toString()}');
  }

  /// Handle generic errors
  void _handleGenericError(dynamic error) {
    _lastError = error.toString();
    addMessage(ChatMessage.assistant(
      'Sorry, something went wrong. Please try again.'
    ));
    debugPrint('Generic Error: $error');
  }

  /// Set loading state
  void _setLoading(bool loading) {
    _isLoading = loading;
    notifyListeners();
  }

  /// Clear all messages
  void clearMessages() {
    _messages.clear();
    _lastFlightResults = null;
    _lastHotelResults = null;
    _lastError = null;
    _currentThreadId = const Uuid().v4();
    notifyListeners();
  }

  /// Retry last message (useful for error recovery)
  Future<void> retryLastMessage() async {
    if (_messages.isNotEmpty && _messages.last.isUser) {
      final lastUserMessage = _messages.last.content;
      await sendMessage(lastUserMessage);
    }
  }

  /// Refresh connection status
  Future<void> refreshConnection() async {
    await _checkConnection();
  }

  @override
  void dispose() {
    _apiService.dispose();
    super.dispose();
  }
}
