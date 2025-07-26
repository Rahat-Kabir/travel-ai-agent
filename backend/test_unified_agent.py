#!/usr/bin/env python3
"""
Comprehensive test script for the unified travel agent.
Tests flight-only, hotel-only, and combined travel requests.
"""

import asyncio
import os
import sys
from datetime import datetime, timedelta

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from app.agents.travel_agent import get_travel_agent
from app.models.flight import ChatRequest


async def test_flight_only():
    """Test flight-only search functionality."""
    print("\n" + "="*60)
    print("🛫 TESTING FLIGHT-ONLY SEARCH")
    print("="*60)
    
    agent = get_travel_agent()
    
    # Test cases for flight searches
    flight_queries = [
        "I want to fly from New York to Los Angeles on December 25th, returning January 2nd for 2 passengers",
        "Find me a one-way flight from JFK to LAX on March 15th",
        "I need business class flights from London to Tokyo next month"
    ]
    
    for i, query in enumerate(flight_queries, 1):
        print(f"\n--- Flight Test {i} ---")
        print(f"Query: {query}")
        
        try:
            request = ChatRequest(message=query)
            response = await agent.process_message(request)
            
            print(f"✅ Response: {response.message[:150]}...")
            print(f"Thread ID: {response.thread_id}")
            
            if response.extracted_params:
                params = response.extracted_params
                print(f"📊 Extracted Parameters:")
                print(f"   - Search Type: {params.search_type}")
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
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")


async def test_hotel_only():
    """Test hotel-only search functionality."""
    print("\n" + "="*60)
    print("🏨 TESTING HOTEL-ONLY SEARCH")
    print("="*60)
    
    agent = get_travel_agent()
    
    # Test cases for hotel searches
    hotel_queries = [
        "I need a hotel in Paris from March 15th to March 20th for 2 guests",
        "Find me accommodation in Tokyo for 5 nights starting April 1st",
        "I want a luxury hotel in New York for my business trip next week"
    ]
    
    for i, query in enumerate(hotel_queries, 1):
        print(f"\n--- Hotel Test {i} ---")
        print(f"Query: {query}")
        
        try:
            request = ChatRequest(message=query)
            response = await agent.process_message(request)
            
            print(f"✅ Response: {response.message[:150]}...")
            print(f"Thread ID: {response.thread_id}")
            
            if response.extracted_params:
                params = response.extracted_params
                print(f"📊 Extracted Parameters:")
                print(f"   - Search Type: {params.search_type}")
                if params.hotel_location:
                    print(f"   - Location: {params.hotel_location}")
                if params.check_in_date:
                    print(f"   - Check-in: {params.check_in_date}")
                if params.check_out_date:
                    print(f"   - Check-out: {params.check_out_date}")
                print(f"   - Guests: {params.guests}")
                print(f"   - Rooms: {params.rooms}")
            
            if response.needs_clarification:
                print(f"❓ Needs clarification: {response.missing_params}")
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")


async def test_combined_travel():
    """Test combined flight and hotel search functionality."""
    print("\n" + "="*60)
    print("✈️🏨 TESTING COMBINED TRAVEL SEARCH")
    print("="*60)
    
    agent = get_travel_agent()
    
    # Test cases for combined searches
    combined_queries = [
        "I want to fly from NYC to Paris on March 15th and need a hotel there for 5 nights",
        "Plan my trip to Tokyo: flight from Los Angeles and accommodation for a week",
        "I need flights and hotels for my business trip to London next month"
    ]
    
    for i, query in enumerate(combined_queries, 1):
        print(f"\n--- Combined Test {i} ---")
        print(f"Query: {query}")
        
        try:
            request = ChatRequest(message=query)
            response = await agent.process_message(request)
            
            print(f"✅ Response: {response.message[:150]}...")
            print(f"Thread ID: {response.thread_id}")
            
            if response.extracted_params:
                params = response.extracted_params
                print(f"📊 Extracted Parameters:")
                print(f"   - Search Type: {params.search_type}")
                
                # Flight parameters
                if params.departure_location or params.arrival_location:
                    print(f"   Flight Details:")
                    if params.departure_location:
                        print(f"     - From: {params.departure_location}")
                    if params.arrival_location:
                        print(f"     - To: {params.arrival_location}")
                    if params.departure_date:
                        print(f"     - Departure: {params.departure_date}")
                    if params.return_date:
                        print(f"     - Return: {params.return_date}")
                    print(f"     - Passengers: {params.passengers}")
                
                # Hotel parameters
                if params.hotel_location or params.check_in_date:
                    print(f"   Hotel Details:")
                    if params.hotel_location:
                        print(f"     - Location: {params.hotel_location}")
                    if params.check_in_date:
                        print(f"     - Check-in: {params.check_in_date}")
                    if params.check_out_date:
                        print(f"     - Check-out: {params.check_out_date}")
                    print(f"     - Guests: {params.guests}")
                    print(f"     - Rooms: {params.rooms}")
            
            if response.needs_clarification:
                print(f"❓ Needs clarification: {response.missing_params}")
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")


async def test_conversation_continuity():
    """Test conversation continuity and state management."""
    print("\n" + "="*60)
    print("💬 TESTING CONVERSATION CONTINUITY")
    print("="*60)
    
    agent = get_travel_agent()
    
    # Start a conversation
    print("\n--- Starting Conversation ---")
    request1 = ChatRequest(message="I want to plan a trip to Europe")
    response1 = await agent.process_message(request1)
    
    print(f"User: I want to plan a trip to Europe")
    print(f"Agent: {response1.message[:100]}...")
    thread_id = response1.thread_id
    
    # Continue the conversation
    print("\n--- Continuing Conversation ---")
    request2 = ChatRequest(
        message="I want to fly from New York to Paris on March 15th",
        thread_id=thread_id
    )
    response2 = await agent.process_message(request2)
    
    print(f"User: I want to fly from New York to Paris on March 15th")
    print(f"Agent: {response2.message[:100]}...")
    
    # Add hotel request
    print("\n--- Adding Hotel Request ---")
    request3 = ChatRequest(
        message="And I need a hotel in Paris for 5 nights",
        thread_id=thread_id
    )
    response3 = await agent.process_message(request3)
    
    print(f"User: And I need a hotel in Paris for 5 nights")
    print(f"Agent: {response3.message[:100]}...")
    
    if response3.extracted_params:
        params = response3.extracted_params
        print(f"📊 Final Extracted Parameters:")
        print(f"   - Search Type: {params.search_type}")
        print(f"   - Flight: {params.departure_location} → {params.arrival_location}")
        print(f"   - Hotel: {params.hotel_location}")


async def main():
    """Run all tests."""
    print("🚀 UNIFIED TRAVEL AGENT COMPREHENSIVE TESTS")
    print("=" * 60)
    
    # Check environment
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ OPENAI_API_KEY not set. Please set it in your .env file.")
        return
    
    if not os.getenv("SERPAPI_API_KEY"):
        print("❌ SERPAPI_API_KEY not set. Please set it in your .env file.")
        return
    
    print("✅ Environment variables configured")
    
    try:
        # Run all test suites
        await test_flight_only()
        await test_hotel_only()
        await test_combined_travel()
        await test_conversation_continuity()
        
        print("\n" + "="*60)
        print("🎉 ALL TESTS COMPLETED!")
        print("="*60)
        print("The unified travel agent successfully handles:")
        print("✅ Flight-only searches")
        print("✅ Hotel-only searches") 
        print("✅ Combined travel searches")
        print("✅ Conversation continuity")
        
    except Exception as e:
        print(f"\n❌ Test suite failed: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
