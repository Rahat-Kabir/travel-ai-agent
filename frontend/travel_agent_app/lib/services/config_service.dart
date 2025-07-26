class ConfigService {
  static const String _defaultBaseUrl = 'http://localhost:8000';
  static const Duration _defaultTimeout = Duration(seconds: 30);
  
  // In a real app, these would come from environment variables or config files
  static String get baseUrl {
    // You can override this for different environments
    const String envUrl = String.fromEnvironment('API_BASE_URL');
    return envUrl.isNotEmpty ? envUrl : _defaultBaseUrl;
  }
  
  static Duration get timeout => _defaultTimeout;
  
  static Map<String, String> get defaultHeaders => {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  };
  
  // API endpoints
  static String get chatEndpoint => '/chat/message';
  static String get healthEndpoint => '/health';
  
  // App configuration
  static const String appName = 'Travel Agent';
  static const String appVersion = '1.0.0';
  
  // UI configuration
  static const Duration splashDuration = Duration(seconds: 3);
  static const Duration typingIndicatorDelay = Duration(milliseconds: 500);
  static const Duration messageAnimationDuration = Duration(milliseconds: 300);
}
