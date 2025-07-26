"""
Server startup script for the Travel Agent API.
"""

import os
import sys
import uvicorn
from pathlib import Path

# Add the app directory to the Python path
sys.path.insert(0, str(Path(__file__).parent))

from app.core.config import get_settings


def main():
    """Start the FastAPI server."""
    
    print("🚀 Starting Travel Agent API Server")
    print("=" * 50)
    
    # Load settings
    try:
        settings = get_settings()
        print(f"✅ Configuration loaded: {settings.api_title} v{settings.api_version}")
    except Exception as e:
        print(f"❌ Configuration error: {str(e)}")
        print("\nPlease ensure your .env file is properly configured with:")
        print("OPENAI_API_KEY=your_openai_key_here")
        print("SERPAPI_API_KEY=your_serpapi_key_here")
        return
    
    # Check required environment variables
    openai_key = os.getenv("OPENAI_API_KEY")
    serpapi_key = os.getenv("SERPAPI_API_KEY")
    
    if not openai_key:
        print("❌ OPENAI_API_KEY is not set")
        return
    
    if not serpapi_key:
        print("❌ SERPAPI_API_KEY is not set")
        return
    
    print(f"✅ API keys configured")
    print(f"🌐 Server will start on http://{settings.host}:{settings.port}")
    print(f"📚 API docs will be available at http://{settings.host}:{settings.port}/docs")
    print(f"🏥 Health check at http://{settings.host}:{settings.port}/health")
    print("\n" + "=" * 50)
    
    # Start the server
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.reload,
        log_level=settings.log_level.lower(),
        access_log=True
    )


if __name__ == "__main__":
    main()
