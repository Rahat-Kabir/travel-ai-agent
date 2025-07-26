import 'package:flutter/material.dart';
import 'package:flutter_animate/flutter_animate.dart';
import '../services/config_service.dart';
import '../services/api_service.dart';
import 'chat_screen.dart';

class SplashScreen extends StatefulWidget {
  const SplashScreen({super.key});

  @override
  State<SplashScreen> createState() => _SplashScreenState();
}

class _SplashScreenState extends State<SplashScreen> {
  String _statusMessage = 'Initializing...';
  final ApiService _apiService = ApiService();

  @override
  void initState() {
    super.initState();
    _initializeApp();
  }

  Future<void> _initializeApp() async {
    // Show splash for minimum duration
    await Future.delayed(const Duration(seconds: 1));

    // Check API health
    setState(() {
      _statusMessage = 'Connecting to travel agent...';
    });

    try {
      await _apiService.checkHealth();
      setState(() {
        _statusMessage = 'Ready to help you travel!';
      });
      
      // Wait a bit more to show success message
      await Future.delayed(const Duration(seconds: 1));
      
      if (mounted) {
        Navigator.of(context).pushReplacement(
          MaterialPageRoute(builder: (context) => const ChatScreen()),
        );
      }
    } catch (e) {
      setState(() {
        _statusMessage = 'Connection failed. Continuing offline...';
      });
      
      // Still navigate to chat screen after a delay
      await Future.delayed(const Duration(seconds: 2));
      
      if (mounted) {
        Navigator.of(context).pushReplacement(
          MaterialPageRoute(builder: (context) => const ChatScreen()),
        );
      }
    }
  }

  @override
  void dispose() {
    _apiService.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        decoration: const BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
            colors: [
              Color(0xFF1E3A8A), // Deep blue
              Color(0xFF3B82F6), // Blue
              Color(0xFF06B6D4), // Cyan
            ],
          ),
        ),
        child: SafeArea(
          child: Column(
            children: [
              Expanded(
                child: Center(
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      // App Icon/Logo
                      Container(
                        width: 120,
                        height: 120,
                        decoration: BoxDecoration(
                          color: Colors.white.withOpacity(0.2),
                          borderRadius: BorderRadius.circular(30),
                          border: Border.all(
                            color: Colors.white.withOpacity(0.3),
                            width: 2,
                          ),
                        ),
                        child: const Icon(
                          Icons.flight_takeoff,
                          size: 60,
                          color: Colors.white,
                        ),
                      )
                          .animate()
                          .scale(
                            duration: 800.ms,
                            curve: Curves.elasticOut,
                          )
                          .fadeIn(duration: 600.ms),

                      const SizedBox(height: 32),

                      // App Title
                      Text(
                        ConfigService.appName,
                        style: const TextStyle(
                          fontSize: 32,
                          fontWeight: FontWeight.bold,
                          color: Colors.white,
                          letterSpacing: 1.2,
                        ),
                      )
                          .animate()
                          .fadeIn(delay: 300.ms, duration: 600.ms)
                          .slideY(begin: 0.3, end: 0),

                      const SizedBox(height: 8),

                      // Subtitle
                      Text(
                        'Your AI Travel Companion',
                        style: TextStyle(
                          fontSize: 16,
                          color: Colors.white.withOpacity(0.9),
                          letterSpacing: 0.5,
                        ),
                      )
                          .animate()
                          .fadeIn(delay: 500.ms, duration: 600.ms)
                          .slideY(begin: 0.3, end: 0),

                      const SizedBox(height: 64),

                      // Loading indicator and status
                      Column(
                        children: [
                          SizedBox(
                            width: 40,
                            height: 40,
                            child: CircularProgressIndicator(
                              strokeWidth: 3,
                              valueColor: AlwaysStoppedAnimation<Color>(
                                Colors.white.withOpacity(0.8),
                              ),
                            ),
                          )
                              .animate(onPlay: (controller) => controller.repeat())
                              .rotate(duration: 1000.ms),

                          const SizedBox(height: 16),

                          Text(
                            _statusMessage,
                            style: TextStyle(
                              fontSize: 14,
                              color: Colors.white.withOpacity(0.8),
                            ),
                          )
                              .animate()
                              .fadeIn(delay: 700.ms, duration: 400.ms),
                        ],
                      ),
                    ],
                  ),
                ),
              ),

              // Footer
              Padding(
                padding: const EdgeInsets.all(24.0),
                child: Text(
                  'Powered by AI • Version ${ConfigService.appVersion}',
                  style: TextStyle(
                    fontSize: 12,
                    color: Colors.white.withOpacity(0.6),
                  ),
                )
                    .animate()
                    .fadeIn(delay: 1000.ms, duration: 600.ms),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
