# Travel Agent AI Chat App

A comprehensive full-stack AI agent chat application built with Python backend and Flutter frontend. The application provides intelligent travel assistance for both flight and hotel searches using advanced AI agents.

## Project Structure

```
travel-agent3/
├── backend/                 # Python backend with FastAPI and LangGraph
│   ├── app/
│   │   ├── api/            # FastAPI routes and endpoints
│   │   ├── models/         # Pydantic models and data structures
│   │   │   ├── flight.py   # Flight search models
│   │   │   ├── hotel.py    # Hotel search models
│   │   │   ├── agent.py    # Agent state models
│   │   │   └── base.py     # Base models and utilities
│   │   ├── services/       # Business logic and services
│   │   │   ├── serpapi_service.py    # Flight search service
│   │   │   └── hotel_service.py      # Hotel search service
│   │   ├── agents/         # LangGraph AI agents
│   │   │   ├── travel_agent.py       # Comprehensive travel agent
│   │   │   ├── flight_agent.py       # Flight-specific agent (legacy)
│   │   │   └── tools.py              # LangGraph tools for search
│   │   └── core/           # Core utilities and configurations
│   ├── tests/              # Backend tests
│   ├── config/             # Configuration files
│   └── pyproject.toml      # Python dependencies and project config
├── frontend/               # Flutter mobile/web application
│   └── travel_agent_app/   # Flutter app
├── docs/                   # Project documentation
└── README.md              # This file
```

## Features

### 🛫 Flight Search
- Intelligent flight search using SerpAPI Google Flights
- Support for one-way, round-trip, and multi-city trips
- Multiple travel classes (economy, premium economy, business, first)
- Advanced filtering options (price, stops, airlines, duration)
- Real-time price insights and carbon emissions data

### 🏨 Hotel Search
- Comprehensive hotel search using SerpAPI Google Hotels
- Support for both hotels and vacation rentals
- Advanced filtering (price range, rating, amenities, hotel class)
- Location-based search with nearby attractions
- Detailed property information and reviews

### 🤖 AI Agent Capabilities
- Natural language understanding for travel queries
- Intelligent routing between flight and hotel searches
- Context-aware conversations with state persistence
- Clarifying questions when information is missing
- Personalized recommendations and travel advice

## Technology Stack

### Backend
- **FastAPI**: Modern, fast web framework for building APIs
- **LangGraph**: Framework for building stateful, multi-actor applications with LLMs
- **LangChain**: Framework for developing applications powered by language models
- **SerpAPI**: Real-time search API for Google Flights and Hotels
- **Pydantic**: Data validation using Python type annotations
- **UV**: Fast Python package installer and resolver

### Frontend
- **Flutter**: Cross-platform UI toolkit for mobile, web, and desktop
- **Dart**: Programming language optimized for building user interfaces

## Getting Started

### Prerequisites
- Python 3.11+
- UV package manager
- Flutter SDK
- Dart SDK
- OpenAI API key
- SerpAPI key

### Environment Setup

1. **Clone the repository**
```bash
git clone <repository-url>
cd travel-agent3
```

2. **Set up environment variables**
Create a `.env` file in the backend directory:
```bash
cd backend
cp .env.example .env
```

Edit `.env` with your API keys:
```
OPENAI_API_KEY=your_openai_api_key_here
SERPAPI_API_KEY=your_serpapi_key_here
```

### Backend Setup
```bash
cd backend
uv sync
uv run uvicorn app.main:app --reload
```

The backend will be available at `http://localhost:8000`

### Frontend Setup
```bash
cd frontend/travel_agent_app
flutter pub get
flutter run
```

## API Usage Examples

### Chat with Travel Agent
```bash
curl -X POST "http://localhost:8000/chat/message" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "I need a flight from New York to Los Angeles on December 15th and a hotel in LA for 3 nights"
  }'
```

### Flight-Only Search (Legacy Endpoint)
```bash
curl -X POST "http://localhost:8000/chat/flight-message" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Find flights from JFK to LAX on 2025-12-15"
  }'
```

### Health Check
```bash
curl "http://localhost:8000/chat/health"
```

## Development

### Backend Development
- Use UV for dependency management
- Follow FastAPI best practices
- Implement AI agents using LangGraph
- Use Pydantic for data validation
- Add new travel services by extending the agent tools

### Frontend Development
- Follow Flutter/Dart conventions
- Implement responsive design
- Connect to backend API endpoints

### Adding New Travel Services
The architecture is designed for easy extensibility:

1. **Create new models** in `app/models/`
2. **Implement service** in `app/services/`
3. **Add tools** in `app/agents/tools.py`
4. **Update agent** to handle new service type
5. **Update API endpoints** if needed

## Testing

### Backend Tests
```bash
cd backend
uv run pytest
```

### Frontend Tests
```bash
cd frontend/travel_agent_app
flutter test
```

### Manual Testing
Test the travel agent with various queries:
- "Find flights from NYC to Paris on January 15th"
- "I need a hotel in Tokyo for 3 nights starting December 20th"
- "Plan a trip from London to Rome with flights and accommodation"

## Architecture

### Agent Design
The application uses a ReAct (Reasoning + Acting) pattern with LangGraph:

- **TravelAgent**: Main agent that handles both flight and hotel searches
- **FlightSearchAgent**: Legacy agent for flight-only searches
- **Tools**: Modular tools for different search types
- **State Management**: Conversation state persistence with checkpointing

### Service Layer
- **SerpAPIService**: Handles flight searches via Google Flights API
- **HotelSerpAPIService**: Handles hotel searches via Google Hotels API
- **Modular Design**: Easy to add new travel services

### API Design
- **RESTful endpoints** with FastAPI
- **Backward compatibility** maintained for existing clients
- **Comprehensive error handling** and validation
- **Health checks** and monitoring

## Contributing

1. Create a feature branch
2. Make your changes
3. Add tests for new functionality
4. Update documentation
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For issues and questions:
1. Check the documentation
2. Search existing issues
3. Create a new issue with detailed information
