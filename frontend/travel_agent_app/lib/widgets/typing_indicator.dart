import 'package:flutter/material.dart';
import 'package:flutter_animate/flutter_animate.dart';

class TypingIndicator extends StatelessWidget {
  const TypingIndicator({super.key});

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    
    return Container(
      margin: const EdgeInsets.only(bottom: 16),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          CircleAvatar(
            radius: 16,
            backgroundColor: theme.primaryColor.withOpacity(0.1),
            child: Icon(
              Icons.smart_toy,
              size: 18,
              color: theme.primaryColor,
            ),
          ),
          const SizedBox(width: 8),
          
          Container(
            padding: const EdgeInsets.symmetric(
              horizontal: 16,
              vertical: 12,
            ),
            decoration: BoxDecoration(
              color: Colors.grey[100],
              borderRadius: BorderRadius.circular(20).copyWith(
                bottomLeft: const Radius.circular(4),
              ),
            ),
            child: Row(
              mainAxisSize: MainAxisSize.min,
              children: [
                _buildDot(0),
                const SizedBox(width: 4),
                _buildDot(1),
                const SizedBox(width: 4),
                _buildDot(2),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildDot(int index) {
    return Container(
      width: 8,
      height: 8,
      decoration: BoxDecoration(
        color: Colors.grey[400],
        shape: BoxShape.circle,
      ),
    )
      .animate(onPlay: (controller) => controller.repeat())
      .scale(
        begin: const Offset(0.8, 0.8),
        end: const Offset(1.2, 1.2),
        duration: 600.ms,
        delay: Duration(milliseconds: index * 200),
      )
      .then()
      .scale(
        begin: const Offset(1.2, 1.2),
        end: const Offset(0.8, 0.8),
        duration: 600.ms,
      );
  }
}
