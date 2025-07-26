import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import '../models/models.dart';

class FlightResultsCard extends StatelessWidget {
  final FlightSearchResponse flightResults;

  const FlightResultsCard({
    super.key,
    required this.flightResults,
  });

  @override
  Widget build(BuildContext context) {
    if (flightResults.flights.isEmpty) {
      return Card(
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Row(
            children: [
              Icon(
                Icons.info_outline,
                color: Colors.orange[600],
              ),
              const SizedBox(width: 12),
              const Expanded(
                child: Text(
                  'No flights found for your search criteria.',
                  style: TextStyle(fontSize: 16),
                ),
              ),
            ],
          ),
        ),
      );
    }

    return Card(
      elevation: 2,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(12),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Header
          Container(
            padding: const EdgeInsets.all(16),
            decoration: BoxDecoration(
              color: Theme.of(context).primaryColor.withOpacity(0.1),
              borderRadius: const BorderRadius.only(
                topLeft: Radius.circular(12),
                topRight: Radius.circular(12),
              ),
            ),
            child: Row(
              children: [
                Icon(
                  Icons.flight_takeoff,
                  color: Theme.of(context).primaryColor,
                ),
                const SizedBox(width: 8),
                Text(
                  'Flight Options',
                  style: TextStyle(
                    fontSize: 18,
                    fontWeight: FontWeight.w600,
                    color: Theme.of(context).primaryColor,
                  ),
                ),
                const Spacer(),
                Text(
                  '${flightResults.flights.length} found',
                  style: TextStyle(
                    fontSize: 14,
                    color: Colors.grey[600],
                  ),
                ),
              ],
            ),
          ),

          // Flight options (show first 3)
          ...flightResults.flights.take(3).map((flight) => 
            FlightOptionTile(flightOption: flight)
          ),

          // Show more button if there are more flights
          if (flightResults.flights.length > 3)
            Padding(
              padding: const EdgeInsets.all(16),
              child: Center(
                child: TextButton(
                  onPressed: () {
                    _showAllFlights(context);
                  },
                  child: Text(
                    'View ${flightResults.flights.length - 3} more flights',
                  ),
                ),
              ),
            ),
        ],
      ),
    );
  }

  void _showAllFlights(BuildContext context) {
    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
      ),
      builder: (context) => DraggableScrollableSheet(
        initialChildSize: 0.8,
        maxChildSize: 0.95,
        minChildSize: 0.5,
        expand: false,
        builder: (context, scrollController) => Column(
          children: [
            Container(
              padding: const EdgeInsets.all(16),
              child: Row(
                children: [
                  const Text(
                    'All Flight Options',
                    style: TextStyle(
                      fontSize: 20,
                      fontWeight: FontWeight.w600,
                    ),
                  ),
                  const Spacer(),
                  IconButton(
                    onPressed: () => Navigator.pop(context),
                    icon: const Icon(Icons.close),
                  ),
                ],
              ),
            ),
            Expanded(
              child: ListView.builder(
                controller: scrollController,
                itemCount: flightResults.flights.length,
                itemBuilder: (context, index) => FlightOptionTile(
                  flightOption: flightResults.flights[index],
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class FlightOptionTile extends StatelessWidget {
  final FlightOption flightOption;

  const FlightOptionTile({
    super.key,
    required this.flightOption,
  });

  @override
  Widget build(BuildContext context) {
    final firstFlight = flightOption.flights.first;
    final lastFlight = flightOption.flights.last;
    
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        border: Border(
          bottom: BorderSide(
            color: Colors.grey[200]!,
            width: 1,
          ),
        ),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Route and time
          Row(
            children: [
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      '${firstFlight.departureAirport.id} → ${lastFlight.arrivalAirport.id}',
                      style: const TextStyle(
                        fontSize: 16,
                        fontWeight: FontWeight.w600,
                      ),
                    ),
                    const SizedBox(height: 4),
                    Text(
                      '${DateFormat('MMM d, HH:mm').format(firstFlight.departureTime)} - ${DateFormat('HH:mm').format(lastFlight.arrivalTime)}',
                      style: TextStyle(
                        fontSize: 14,
                        color: Colors.grey[600],
                      ),
                    ),
                  ],
                ),
              ),
              Column(
                crossAxisAlignment: CrossAxisAlignment.end,
                children: [
                  Text(
                    '${flightOption.currency} ${flightOption.price.toStringAsFixed(0)}',
                    style: const TextStyle(
                      fontSize: 18,
                      fontWeight: FontWeight.bold,
                      color: Colors.green,
                    ),
                  ),
                  Text(
                    _formatDuration(flightOption.totalDuration),
                    style: TextStyle(
                      fontSize: 12,
                      color: Colors.grey[600],
                    ),
                  ),
                ],
              ),
            ],
          ),

          const SizedBox(height: 8),

          // Flight details
          Row(
            children: [
              Icon(
                Icons.flight,
                size: 16,
                color: Colors.grey[600],
              ),
              const SizedBox(width: 4),
              Text(
                firstFlight.airline,
                style: TextStyle(
                  fontSize: 12,
                  color: Colors.grey[600],
                ),
              ),
              const SizedBox(width: 16),
              if (flightOption.layovers.isNotEmpty) ...[
                Icon(
                  Icons.connecting_airports,
                  size: 16,
                  color: Colors.grey[600],
                ),
                const SizedBox(width: 4),
                Text(
                  '${flightOption.layovers.length} stop${flightOption.layovers.length > 1 ? 's' : ''}',
                  style: TextStyle(
                    fontSize: 12,
                    color: Colors.grey[600],
                  ),
                ),
              ] else ...[
                Icon(
                  Icons.flight_takeoff,
                  size: 16,
                  color: Colors.green[600],
                ),
                const SizedBox(width: 4),
                Text(
                  'Direct',
                  style: TextStyle(
                    fontSize: 12,
                    color: Colors.green[600],
                    fontWeight: FontWeight.w500,
                  ),
                ),
              ],
            ],
          ),
        ],
      ),
    );
  }

  String _formatDuration(int minutes) {
    final hours = minutes ~/ 60;
    final mins = minutes % 60;
    return '${hours}h ${mins}m';
  }
}
