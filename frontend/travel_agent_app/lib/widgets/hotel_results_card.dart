import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import '../models/models.dart';

class HotelResultsCard extends StatelessWidget {
  final HotelSearchResponse hotelResults;

  const HotelResultsCard({
    super.key,
    required this.hotelResults,
  });

  @override
  Widget build(BuildContext context) {
    if (hotelResults.properties.isEmpty) {
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
                  'No hotels found for your search criteria.',
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
                  Icons.hotel,
                  color: Theme.of(context).primaryColor,
                ),
                const SizedBox(width: 8),
                Text(
                  'Hotel Options',
                  style: TextStyle(
                    fontSize: 18,
                    fontWeight: FontWeight.w600,
                    color: Theme.of(context).primaryColor,
                  ),
                ),
                const Spacer(),
                Text(
                  '${hotelResults.properties.length} found',
                  style: TextStyle(
                    fontSize: 14,
                    color: Colors.grey[600],
                  ),
                ),
              ],
            ),
          ),

          // Hotel properties (show first 3)
          ...hotelResults.properties.take(3).map((property) => 
            HotelPropertyTile(hotelProperty: property)
          ),

          // Show more button if there are more hotels
          if (hotelResults.properties.length > 3)
            Padding(
              padding: const EdgeInsets.all(16),
              child: Center(
                child: TextButton(
                  onPressed: () {
                    _showAllHotels(context);
                  },
                  child: Text(
                    'View ${hotelResults.properties.length - 3} more hotels',
                  ),
                ),
              ),
            ),
        ],
      ),
    );
  }

  void _showAllHotels(BuildContext context) {
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
                    'All Hotel Options',
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
                itemCount: hotelResults.properties.length,
                itemBuilder: (context, index) => HotelPropertyTile(
                  hotelProperty: hotelResults.properties[index],
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class HotelPropertyTile extends StatelessWidget {
  final HotelProperty hotelProperty;

  const HotelPropertyTile({
    super.key,
    required this.hotelProperty,
  });

  @override
  Widget build(BuildContext context) {
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
          // Hotel name and rating
          Row(
            children: [
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      hotelProperty.name,
                      style: const TextStyle(
                        fontSize: 16,
                        fontWeight: FontWeight.w600,
                      ),
                    ),
                    const SizedBox(height: 4),
                    Row(
                      children: [
                        if (hotelProperty.extractedHotelClass != null) ...[
                          ...List.generate(
                            hotelProperty.extractedHotelClass!,
                            (index) => Icon(
                              Icons.star,
                              size: 16,
                              color: Colors.amber[600],
                            ),
                          ),
                          const SizedBox(width: 8),
                        ],
                        if (hotelProperty.overallRating != null) ...[
                          Icon(
                            Icons.star,
                            size: 16,
                            color: Colors.green[600],
                          ),
                          const SizedBox(width: 4),
                          Text(
                            hotelProperty.overallRating!.toStringAsFixed(1),
                            style: TextStyle(
                              fontSize: 14,
                              fontWeight: FontWeight.w500,
                              color: Colors.green[600],
                            ),
                          ),
                          const SizedBox(width: 4),
                          if (hotelProperty.reviews != null)
                            Text(
                              '(${hotelProperty.reviews})',
                              style: TextStyle(
                                fontSize: 12,
                                color: Colors.grey[600],
                              ),
                            ),
                        ],
                      ],
                    ),
                  ],
                ),
              ),
              Column(
                crossAxisAlignment: CrossAxisAlignment.end,
                children: [
                  if (hotelProperty.ratePerNight?.extractedLowest != null) ...[
                    Text(
                      '\$${hotelProperty.ratePerNight!.extractedLowest!.toStringAsFixed(0)}',
                      style: const TextStyle(
                        fontSize: 18,
                        fontWeight: FontWeight.bold,
                        color: Colors.green,
                      ),
                    ),
                    Text(
                      'per night',
                      style: TextStyle(
                        fontSize: 12,
                        color: Colors.grey[600],
                      ),
                    ),
                  ] else if (hotelProperty.ratePerNight?.lowest != null) ...[
                    Text(
                      hotelProperty.ratePerNight!.lowest!,
                      style: const TextStyle(
                        fontSize: 16,
                        fontWeight: FontWeight.bold,
                        color: Colors.green,
                      ),
                    ),
                    Text(
                      'per night',
                      style: TextStyle(
                        fontSize: 12,
                        color: Colors.grey[600],
                      ),
                    ),
                  ],
                ],
              ),
            ],
          ),

          const SizedBox(height: 8),

          // Amenities and features
          Wrap(
            children: [
              if (hotelProperty.ecoCertified) ...[
                _buildFeatureChip(
                  icon: Icons.eco,
                  label: 'Eco-certified',
                  color: Colors.green,
                ),
                const SizedBox(width: 8),
              ],
              if (hotelProperty.sponsored) ...[
                _buildFeatureChip(
                  icon: Icons.workspace_premium,
                  label: 'Sponsored',
                  color: Colors.orange,
                ),
                const SizedBox(width: 8),
              ],
              if (hotelProperty.amenities.contains('Free Wi-Fi') ||
                  hotelProperty.amenities.contains('WiFi')) ...[
                _buildFeatureChip(
                  icon: Icons.wifi,
                  label: 'Free WiFi',
                  color: Colors.blue,
                ),
                const SizedBox(width: 8),
              ],
              if (hotelProperty.amenities.contains('Free parking') ||
                  hotelProperty.amenities.contains('Parking')) ...[
                _buildFeatureChip(
                  icon: Icons.local_parking,
                  label: 'Parking',
                  color: Colors.blue,
                ),
                const SizedBox(width: 8),
              ],
              if (hotelProperty.amenities.contains('Pool') ||
                  hotelProperty.amenities.contains('Swimming pool')) ...[
                _buildFeatureChip(
                  icon: Icons.pool,
                  label: 'Pool',
                  color: Colors.blue,
                ),
                const SizedBox(width: 8),
              ],
              if (hotelProperty.amenities.contains('Gym') ||
                  hotelProperty.amenities.contains('Fitness center')) ...[
                _buildFeatureChip(
                  icon: Icons.fitness_center,
                  label: 'Gym',
                  color: Colors.blue,
                ),
                const SizedBox(width: 8),
              ],
            ],
          ),

          // Show first few amenities if none of the common ones are found
          if (!hotelProperty.amenities.any((amenity) => 
              ['Free Wi-Fi', 'WiFi', 'Free parking', 'Parking', 'Pool', 
               'Swimming pool', 'Gym', 'Fitness center'].contains(amenity)) &&
              hotelProperty.amenities.isNotEmpty) ...[
            const SizedBox(height: 4),
            Text(
              hotelProperty.amenities.take(3).join(' • '),
              style: TextStyle(
                fontSize: 12,
                color: Colors.grey[600],
              ),
              maxLines: 1,
              overflow: TextOverflow.ellipsis,
            ),
          ],

          // Location info
          if (hotelProperty.nearbyPlaces.isNotEmpty) ...[
            const SizedBox(height: 4),
            Row(
              children: [
                Icon(
                  Icons.location_on,
                  size: 14,
                  color: Colors.grey[600],
                ),
                const SizedBox(width: 4),
                Expanded(
                  child: Text(
                    hotelProperty.nearbyPlaces.first.name,
                    style: TextStyle(
                      fontSize: 12,
                      color: Colors.grey[600],
                    ),
                    overflow: TextOverflow.ellipsis,
                  ),
                ),
                if (hotelProperty.nearbyPlaces.first.transportations.isNotEmpty)
                  Text(
                    hotelProperty.nearbyPlaces.first.transportations.first.duration,
                    style: TextStyle(
                      fontSize: 12,
                      color: Colors.grey[600],
                    ),
                  ),
              ],
            ),
          ],
        ],
      ),
    );
  }

  Widget _buildFeatureChip({
    required IconData icon,
    required String label,
    required Color color,
  }) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
      decoration: BoxDecoration(
        color: color.withOpacity(0.1),
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: color.withOpacity(0.3)),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(
            icon,
            size: 12,
            color: color,
          ),
          const SizedBox(width: 4),
          Text(
            label,
            style: TextStyle(
              fontSize: 10,
              fontWeight: FontWeight.w500,
              color: color,
            ),
          ),
        ],
      ),
    );
  }
}