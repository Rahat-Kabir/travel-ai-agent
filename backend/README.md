# Travel Agent Backend

AI-powered unified travel search agent built with FastAPI, LangGraph, and SerpAPI. This backend provides intelligent flight and hotel search capabilities through a conversational AI interface.

## ✨ Features

- **Unified Travel Search**: Natural language search for both flights and hotels using Google Flights and Google Hotels via SerpAPI
- **Conversational AI**: ReAct (Reasoning + Acting) agent pattern for intelligent responses
- **State Management**: Persistent conversation state with LangGraph checkpointing
- **Parameter Extraction**: Automatic extraction of travel search parameters from user queries
- **Clarification Handling**: Smart clarification questions when information is missing
- **Real-time Results**: Fast search with price insights and recommendations for both flights and hotels
- **Intelligent Routing**: Automatically determines whether users need flights, hotels, or both based on their queries

## 🚀 Quick Start

1. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env and add your API keys:
   # OPENAI_API_KEY=your_openai_key_here
   # SERPAPI_API_KEY=your_serpapi_key_here
   ```

2. **Install dependencies**:
   ```bash
   uv sync
   ```

3. **Test the agent**:
   ```bash
   uv run python test_agent.py
   ```

4. **Start the server**:
   ```bash
   uv run python run_server.py
   # Or use uvicorn directly:
   # uv run uvicorn app.main:app --reload
   ```

5. **Access the API**:
   - API Documentation: http://localhost:8000/docs
   - Health Check: http://localhost:8000/health
   - Chat Endpoint: http://localhost:8000/chat/message

## 🏗️ Architecture

### Directory Structure
```
backend/
├── app/
│   ├── api/                # FastAPI routes and endpoints
│   │   ├── chat.py         # Chat endpoints for agent interaction
│   │   └── health.py       # Health check endpoints
│   ├── models/             # Pydantic models
│   │   ├── flight.py       # Flight search models
│   │   ├── hotel.py        # Hotel search models
│   │   ├── agent.py        # Agent state models
│   │   └── base.py         # Base models and utilities
│   ├── services/           # External service integrations
│   │   ├── serpapi_service.py # SerpAPI flight search service
│   │   └── hotel_service.py   # SerpAPI hotel search service
│   ├── agents/             # LangGraph AI agents
│   │   ├── travel_agent.py # Unified travel search agent (ReAct)
│   │   ├── flight_agent.py # Legacy flight search agent
│   │   └── tools.py        # LangGraph tools for travel search
│   ├── core/               # Core utilities
│   │   ├── config.py       # Configuration management
│   │   ├── dependencies.py # FastAPI dependencies
│   │   └── exceptions.py   # Custom exceptions
│   └── main.py             # FastAPI application entry point
├── tests/                  # Test files
├── test_agent.py          # Agent testing script
├── run_server.py          # Server startup script
├── .env.example           # Environment variables template
└── README.md              # This file
```

## 🛠️ Technology Stack

- **FastAPI**: Modern, fast web framework for building APIs with Python
- **LangGraph**: Framework for building stateful, multi-actor applications with LLMs
- **LangChain**: Framework for developing applications powered by language models
- **Pydantic**: Data validation using Python type annotations
- **SerpAPI**: Google Flights and Google Hotels search integration
- **UV**: Fast Python package installer and resolver
- **Uvicorn**: ASGI server for running FastAPI applications

## 📡 API Usage

### Chat with the Travel Agent

#### Flight Search Example
```bash
curl -X POST "http://localhost:8000/chat/message" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "I want to fly from New York to Los Angeles on December 25th, returning January 2nd for 2 passengers"
  }'
```

#### Hotel Search Example
```bash
curl -X POST "http://localhost:8000/chat/message" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "I need a hotel in Paris from March 15th to March 20th for 2 guests"
  }'
```

#### Combined Travel Search Example
```bash
curl -X POST "http://localhost:8000/chat/message" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "I want to fly from NYC to Paris on March 15th and need a hotel there for 5 nights"
  }'
```

### Example Response

```json
{
  "message": "I found several travel options for your trip...",
  "thread_id": "thread_1234567890",
  "flight_results": {
    "best_flights": [...],
    "price_insights": {...}
  },
  "hotel_results": {
    "properties": [...],
    "search_metadata": {...}
  },
  "extracted_params": {
    "search_type": "both",
    "departure_location": "New York",
    "arrival_location": "Los Angeles",
    "departure_date": "2024-12-25",
    "return_date": "2025-01-02",
    "passengers": 2,
    "hotel_location": "Los Angeles",
    "check_in_date": "2024-12-25",
    "check_out_date": "2025-01-02",
    "guests": 2
  },
  "needs_clarification": false,
  "missing_params": []
}
```

## 🧪 Development Dependencies

- **pytest**: Testing framework
- **pytest-asyncio**: Async testing support
- **httpx**: HTTP client for testing
- **black**: Code formatter
- **isort**: Import sorter
- **mypy**: Static type checker

## Setup and Installation

1. **Install UV** (if not already installed):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Install dependencies**:
   ```bash
   uv sync
   ```

3. **Activate virtual environment**:
   ```bash
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

## Running the Application

### Development Server
```bash
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Production Server
```bash
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## API Documentation

Once the server is running, you can access:
- **Interactive API docs**: http://localhost:8000/docs
- **ReDoc documentation**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## Testing

### Run all tests
```bash
uv run pytest
```

### Run tests with coverage
```bash
uv run pytest --cov=app
```

### Run specific test file
```bash
uv run pytest tests/test_chat.py
```

## Code Quality

### Format code
```bash
uv run black app tests
```

### Sort imports
```bash
uv run isort app tests
```

### Type checking
```bash
uv run mypy app
```

## Environment Variables

Create a `.env` file in the backend directory:
```env
# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=True

# AI/LLM Configuration
OPENAI_API_KEY=your_openai_api_key_here
LANGCHAIN_API_KEY=your_langchain_api_key_here

# Database Configuration (if needed)
DATABASE_URL=sqlite:///./travel_agent.db
```

## Contributing

1. Follow PEP 8 style guidelines
2. Use type hints for all functions
3. Write tests for new features
4. Update documentation as needed
5. Run code quality checks before committing