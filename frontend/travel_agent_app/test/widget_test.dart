// This is a basic Flutter widget test for the Travel Agent app.

import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

import 'package:travel_agent_app/main.dart';

void main() {
  testWidgets('Travel Agent app smoke test', (WidgetTester tester) async {
    // Build our app and trigger a frame.
    await tester.pumpWidget(const TravelAgentApp());

    // Verify that the splash screen loads
    expect(find.text('Travel Agent'), findsOneWidget);
    expect(find.text('Your AI Travel Companion'), findsOneWidget);
  });
}
