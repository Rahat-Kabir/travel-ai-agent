# Travel Agent Frontend

Flutter frontend for the Travel Agent AI Chat App.

## Overview

This Flutter application provides a cross-platform mobile and web interface for interacting with the Travel Agent AI backend. Users can chat with AI agents to get travel recommendations, book trips, and manage their travel plans.

## Project Structure

```
frontend/
└── travel_agent_app/       # Flutter application
    ├── lib/
    │   ├── main.dart       # Application entry point
    │   ├── models/         # Data models
    │   ├── services/       # API services and HTTP clients
    │   ├── screens/        # UI screens/pages
    │   ├── widgets/        # Reusable UI components
    │   ├── providers/      # State management (Provider/Riverpod)
    │   └── utils/          # Utility functions and constants
    ├── test/               # Unit and widget tests
    ├── integration_test/   # Integration tests
    ├── assets/             # Images, fonts, and other assets
    ├── android/            # Android-specific configuration
    ├── ios/                # iOS-specific configuration
    ├── web/                # Web-specific configuration
    ├── pubspec.yaml        # Flutter dependencies
    └── README.md           # Flutter app specific documentation
```

## Technology Stack

- **Flutter**: Google's UI toolkit for building natively compiled applications
- **Dart**: Programming language optimized for building user interfaces
- **HTTP**: For API communication with the backend
- **Provider/Riverpod**: State management (to be determined)
- **Flutter Secure Storage**: For secure local data storage

## Features (Planned)

- 🤖 AI Chat Interface
- 🗺️ Travel Recommendations
- 📅 Trip Planning
- 💾 Chat History
- 🔐 User Authentication
- 📱 Cross-platform (iOS, Android, Web)
- 🎨 Responsive Design
- 🌙 Dark/Light Theme Support

## Prerequisites

- Flutter SDK (3.0+)
- Dart SDK (3.0+)
- Android Studio / Xcode (for mobile development)
- VS Code with Flutter extension (recommended)

## Setup and Installation

1. **Install Flutter**: Follow the official [Flutter installation guide](https://docs.flutter.dev/get-started/install)

2. **Verify installation**:
   ```bash
   flutter doctor
   ```

3. **Navigate to the Flutter app**:
   ```bash
   cd travel_agent_app
   ```

4. **Install dependencies**:
   ```bash
   flutter pub get
   ```

## Running the Application

### Development Mode
```bash
flutter run
```

### Specific Platform
```bash
# Run on Android
flutter run -d android

# Run on iOS
flutter run -d ios

# Run on Web
flutter run -d chrome

# Run on Desktop (Windows/macOS/Linux)
flutter run -d windows
flutter run -d macos
flutter run -d linux
```

### Release Mode
```bash
flutter run --release
```

## Building the Application

### Android APK
```bash
flutter build apk
```

### Android App Bundle
```bash
flutter build appbundle
```

### iOS
```bash
flutter build ios
```

### Web
```bash
flutter build web
```

### Desktop
```bash
flutter build windows
flutter build macos
flutter build linux
```

## Testing

### Unit Tests
```bash
flutter test
```

### Integration Tests
```bash
flutter test integration_test/
```

### Widget Tests
```bash
flutter test test/widget_test.dart
```

## Code Quality

### Analyze Code
```bash
flutter analyze
```

### Format Code
```bash
dart format .
```

## Configuration

### Environment Variables
Create environment-specific configuration files:
- `lib/config/dev_config.dart` - Development configuration
- `lib/config/prod_config.dart` - Production configuration

### API Configuration
Update the API base URL in the configuration files to point to your backend:
```dart
class ApiConfig {
  static const String baseUrl = 'http://localhost:8000'; // Development
  // static const String baseUrl = 'https://your-api.com'; // Production
}
```

## Development Guidelines

1. **Code Structure**: Follow Flutter/Dart conventions
2. **State Management**: Use Provider or Riverpod for state management
3. **API Integration**: Create service classes for backend communication
4. **UI Components**: Build reusable widgets
5. **Testing**: Write unit tests for business logic and widget tests for UI
6. **Documentation**: Document complex widgets and business logic

## Useful Commands

```bash
# Clean build files
flutter clean

# Get dependencies
flutter pub get

# Upgrade dependencies
flutter pub upgrade

# Check for outdated dependencies
flutter pub outdated

# Generate code (if using code generation)
flutter packages pub run build_runner build

# Run with specific flavor
flutter run --flavor dev
flutter run --flavor prod
```

## Contributing

1. Follow Flutter/Dart style guidelines
2. Use meaningful widget and variable names
3. Write tests for new features
4. Update documentation as needed
5. Ensure responsive design across different screen sizes

## Resources

- [Flutter Documentation](https://docs.flutter.dev/)
- [Dart Documentation](https://dart.dev/guides)
- [Flutter Cookbook](https://docs.flutter.dev/cookbook)
- [Flutter Widget Catalog](https://docs.flutter.dev/development/ui/widgets)
