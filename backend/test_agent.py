"""
Test script for the flight search agent.
"""

import asyncio
import os
import sys
from pathlib import Path

# Add the app directory to the Python path
sys.path.insert(0, str(Path(__file__).parent))

from app.agents.flight_agent import FlightSearchAgent
from app.models.flight import ChatRequest
from app.core.config import get_settings


async def test_agent():
    """Test the flight search agent with sample queries."""
    
    print("🚀 Testing Travel Agent Flight Search")
    print("=" * 50)
    
    # Check environment variables
    print("\n📋 Environment Check:")
    openai_key = os.getenv("OPENAI_API_KEY")
    serpapi_key = os.getenv("SERPAPI_API_KEY")
    
    print(f"OpenAI API Key: {'✅ Set' if openai_key else '❌ Missing'}")
    print(f"SerpAPI Key: {'✅ Set' if serpapi_key else '❌ Missing'}")
    
    if not openai_key or not serpapi_key:
        print("\n❌ Missing required API keys. Please set them in your .env file:")
        print("OPENAI_API_KEY=your_openai_key_here")
        print("SERPAPI_API_KEY=your_serpapi_key_here")
        return
    
    try:
        # Initialize the agent
        print("\n🤖 Initializing Flight Search Agent...")
        agent = FlightSearchAgent()
        print("✅ Agent initialized successfully")
        
        # Test queries with future dates (after July 23, 2025)
        test_queries = [
            "I want to fly from New York to Los Angeles on December 15th, 2025, returning December 22nd, 2025",
            "Find flights from JFK to LAX for 2 passengers on August 10th, 2025",
            "What are the cheapest flights from London to Paris on September 5th, 2025?",
            "I need a one-way ticket from San Francisco to Chicago on October 30th, 2025"
        ]
        
        print(f"\n💬 Testing {len(test_queries)} sample queries:")
        print("-" * 50)
        
        for i, query in enumerate(test_queries, 1):
            print(f"\n🔍 Test {i}: {query}")
            
            try:
                # Create chat request
                request = ChatRequest(message=query)
                
                # Process the message
                response = await agent.process_message(request)
                
                print(f"✅ Response received (Thread: {response.thread_id})")
                print(f"📝 Agent Reply: {response.message[:200]}...")
                
                if response.extracted_params:
                    print(f"📊 Extracted Parameters:")
                    params = response.extracted_params
                    if params.departure_location:
                        print(f"   - From: {params.departure_location}")
                    if params.arrival_location:
                        print(f"   - To: {params.arrival_location}")
                    if params.departure_date:
                        print(f"   - Departure: {params.departure_date}")
                    if params.return_date:
                        print(f"   - Return: {params.return_date}")
                    print(f"   - Passengers: {params.passengers}")
                
                if response.needs_clarification:
                    print(f"❓ Needs clarification: {response.missing_params}")
                
                if response.flight_results:
                    print(f"✈️ Flight results available")
                
            except Exception as e:
                print(f"❌ Error processing query: {str(e)}")
            
            print("-" * 30)
        
        print("\n🎉 Agent testing completed!")
        
    except Exception as e:
        print(f"❌ Failed to initialize agent: {str(e)}")
        import traceback
        traceback.print_exc()


async def test_tools():
    """Test the flight search tools directly."""
    
    print("\n🔧 Testing Flight Search Tools")
    print("=" * 50)
    
    try:
        from app.agents.tools import search_flights, get_airport_suggestions
        
        # Test airport suggestions
        print("\n🏢 Testing airport suggestions:")
        suggestions_result = get_airport_suggestions.invoke({"location_query": "New York"})
        print(f"NYC suggestions: {suggestions_result}")
        
        # Test flight search (this will make an actual API call)
        print("\n✈️ Testing flight search:")
        print("Note: This will make a real SerpAPI call and may take a few seconds...")
        
        flight_result = search_flights.invoke({
            "departure_location": "JFK",
            "arrival_location": "LAX",
            "departure_date": "2025-12-15",
            "return_date": "2025-12-22",
            "passengers": 1,
            "trip_type": "round_trip",
            "travel_class": "economy"
        })
        
        print(f"Flight search result: {flight_result[:500]}...")
        
    except Exception as e:
        print(f"❌ Error testing tools: {str(e)}")
        import traceback
        traceback.print_exc()


def main():
    """Main test function."""
    print("🧪 Travel Agent Backend Test Suite")
    print("=" * 60)
    
    # Test configuration
    try:
        settings = get_settings()
        print(f"✅ Configuration loaded: {settings.api_title}")
    except Exception as e:
        print(f"❌ Configuration error: {str(e)}")
        return
    
    # Run async tests
    asyncio.run(test_agent())
    
    # Test tools
    asyncio.run(test_tools())
    
    print("\n" + "=" * 60)
    print("🏁 Test suite completed!")
    print("\nTo start the API server, run:")
    print("uv run uvicorn app.main:app --reload")


if __name__ == "__main__":
    main()
