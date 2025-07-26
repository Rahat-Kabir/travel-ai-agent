import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import '../models/models.dart';
import 'flight_results_card.dart';

class MessageBubble extends StatelessWidget {
  final ChatMessage message;
  final FlightSearchResponse? flightResults;

  const MessageBubble({
    super.key,
    required this.message,
    this.flightResults,
  });

  @override
  Widget build(BuildContext context) {
    final isUser = message.isUser;
    final theme = Theme.of(context);
    
    return Container(
      margin: const EdgeInsets.only(bottom: 16),
      child: Column(
        crossAxisAlignment: 
          isUser ? CrossAxisAlignment.end : CrossAxisAlignment.start,
        children: [
          Row(
            mainAxisAlignment: 
              isUser ? MainAxisAlignment.end : MainAxisAlignment.start,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              if (!isUser) ...[
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
              ],
              
              Flexible(
                child: Container(
                  padding: const EdgeInsets.symmetric(
                    horizontal: 16,
                    vertical: 12,
                  ),
                  decoration: BoxDecoration(
                    color: isUser 
                      ? theme.primaryColor 
                      : Colors.grey[100],
                    borderRadius: BorderRadius.circular(20).copyWith(
                      bottomRight: isUser ? const Radius.circular(4) : null,
                      bottomLeft: !isUser ? const Radius.circular(4) : null,
                    ),
                  ),
                  child: Text(
                    message.content,
                    style: TextStyle(
                      color: isUser ? Colors.white : Colors.black87,
                      fontSize: 16,
                      height: 1.4,
                    ),
                  ),
                ),
              ),
              
              if (isUser) ...[
                const SizedBox(width: 8),
                CircleAvatar(
                  radius: 16,
                  backgroundColor: theme.primaryColor,
                  child: const Icon(
                    Icons.person,
                    size: 18,
                    color: Colors.white,
                  ),
                ),
              ],
            ],
          ),
          
          // Timestamp
          Padding(
            padding: EdgeInsets.only(
              top: 4,
              left: isUser ? 0 : 40,
              right: isUser ? 40 : 0,
            ),
            child: Text(
              DateFormat('HH:mm').format(message.timestamp),
              style: TextStyle(
                fontSize: 12,
                color: Colors.grey[600],
              ),
            ),
          ),
          
          // Flight results (only for assistant messages)
          if (!isUser && flightResults != null) ...[
            const SizedBox(height: 12),
            Padding(
              padding: const EdgeInsets.only(left: 40),
              child: FlightResultsCard(flightResults: flightResults!),
            ),
          ],
        ],
      ),
    );
  }
}
