import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import 'package:flutter_markdown/flutter_markdown.dart';
import '../models/models.dart';
import 'flight_results_card.dart';
import 'hotel_results_card.dart';

class MessageBubble extends StatelessWidget {
  final ChatMessage message;
  final FlightSearchResponse? flightResults;
  final HotelSearchResponse? hotelResults;

  const MessageBubble({
    super.key,
    required this.message,
    this.flightResults,
    this.hotelResults,
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
                  child: MarkdownBody(
                    data: message.content,
                    shrinkWrap: true,
                    styleSheet: MarkdownStyleSheet(
                      p: TextStyle(
                        color: isUser ? Colors.white : Colors.black87,
                        fontSize: 16,
                        height: 1.4,
                      ),
                      h1: TextStyle(
                        color: isUser ? Colors.white : Colors.black87,
                        fontSize: 24,
                        fontWeight: FontWeight.bold,
                        height: 1.2,
                      ),
                      h2: TextStyle(
                        color: isUser ? Colors.white : Colors.black87,
                        fontSize: 20,
                        fontWeight: FontWeight.bold,
                        height: 1.2,
                      ),
                      h3: TextStyle(
                        color: isUser ? Colors.white : Colors.black87,
                        fontSize: 18,
                        fontWeight: FontWeight.w600,
                        height: 1.2,
                      ),
                      strong: TextStyle(
                        color: isUser ? Colors.white : Colors.black87,
                        fontWeight: FontWeight.bold,
                      ),
                      em: TextStyle(
                        color: isUser ? Colors.white : Colors.black87,
                        fontStyle: FontStyle.italic,
                      ),
                      a: TextStyle(
                        color: isUser ? Colors.white70 : Colors.blue,
                        decoration: TextDecoration.underline,
                      ),
                      code: TextStyle(
                        color: isUser ? Colors.white : Colors.black87,
                        backgroundColor: isUser ? Colors.white.withOpacity(0.1) : Colors.grey.withOpacity(0.1),
                        fontFamily: 'monospace',
                      ),
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
          
          // Hotel results (only for assistant messages)
          if (!isUser && hotelResults != null) ...[
            const SizedBox(height: 12),
            Padding(
              padding: const EdgeInsets.only(left: 40),
              child: HotelResultsCard(hotelResults: hotelResults!),
            ),
          ],
        ],
      ),
    );
  }
}
