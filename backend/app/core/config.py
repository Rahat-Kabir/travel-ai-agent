"""
Configuration settings for the Travel Agent API.
"""

import os
import logging
from typing import List, Optional
from pydantic import Field
from pydantic_settings import BaseSettings

from ..models.base import APIConfig, ExternalAPIConfig, LoggingConfig


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # API Configuration
    api_title: str = Field("Travel Agent API", env="API_TITLE")
    api_description: str = Field(
        "AI-powered flight search and travel planning API",
        env="API_DESCRIPTION"
    )
    api_version: str = Field("1.0.0", env="API_VERSION")
    debug: bool = Field(False, env="DEBUG")
    
    # Server Configuration
    host: str = Field("0.0.0.0", env="API_HOST")
    port: int = Field(8000, env="API_PORT")
    reload: bool = Field(False, env="API_RELOAD")
    
    # CORS Configuration
    cors_origins: List[str] = Field(
        default_factory=lambda: ["*"],
        env="CORS_ORIGINS"
    )
    cors_methods: List[str] = Field(
        default_factory=lambda: ["*"],
        env="CORS_METHODS"
    )
    cors_headers: List[str] = Field(
        default_factory=lambda: ["*"],
        env="CORS_HEADERS"
    )
    
    # External API Keys
    openai_api_key: str = Field(..., env="OPENAI_API_KEY")
    serpapi_api_key: str = Field(..., env="SERPAPI_API_KEY")
    langchain_api_key: Optional[str] = Field(None, env="LANGCHAIN_API_KEY")
    
    # OpenAI Configuration
    openai_model: str = Field("gpt-4.1-mini", env="OPENAI_MODEL")
    openai_temperature: float = Field(0.1, env="OPENAI_TEMPERATURE")
    openai_max_tokens: int = Field(1000, env="OPENAI_MAX_TOKENS")
    
    # SerpAPI Configuration
    serpapi_timeout: int = Field(30, env="SERPAPI_TIMEOUT")
    
    # Rate Limiting
    rate_limit_requests: int = Field(100, env="RATE_LIMIT_REQUESTS")
    rate_limit_window: int = Field(3600, env="RATE_LIMIT_WINDOW")
    
    # Request/Response Settings
    max_request_size: int = Field(1024 * 1024, env="MAX_REQUEST_SIZE")  # 1MB
    request_timeout: int = Field(30, env="REQUEST_TIMEOUT")
    
    # Logging Configuration
    log_level: str = Field("INFO", env="LOG_LEVEL")
    log_format: str = Field(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        env="LOG_FORMAT"
    )
    log_file: Optional[str] = Field(None, env="LOG_FILE")
    
    # Agent Configuration
    agent_max_retries: int = Field(3, env="AGENT_MAX_RETRIES")
    agent_conversation_memory_limit: int = Field(20, env="AGENT_MEMORY_LIMIT")
    
    # Security
    valid_api_keys: Optional[str] = Field(None, env="VALID_API_KEYS")
    
    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": False,
        "extra": "ignore"  # Allow extra fields to be ignored
    }
    
    def get_api_config(self) -> APIConfig:
        """Get API configuration."""
        return APIConfig(
            title=self.api_title,
            description=self.api_description,
            version=self.api_version,
            debug=self.debug,
            cors_origins=self.cors_origins,
            cors_methods=self.cors_methods,
            cors_headers=self.cors_headers,
            rate_limit_requests=self.rate_limit_requests,
            rate_limit_window=self.rate_limit_window,
            max_request_size=self.max_request_size,
            request_timeout=self.request_timeout
        )
    
    def get_external_api_config(self) -> ExternalAPIConfig:
        """Get external API configuration."""
        return ExternalAPIConfig(
            serpapi_key=self.serpapi_api_key,
            serpapi_timeout=self.serpapi_timeout,
            openai_api_key=self.openai_api_key,
            openai_model=self.openai_model,
            openai_temperature=self.openai_temperature,
            openai_max_tokens=self.openai_max_tokens
        )
    
    def get_logging_config(self) -> LoggingConfig:
        """Get logging configuration."""
        return LoggingConfig(
            level=self.log_level,
            format=self.log_format,
            file_path=self.log_file
        )
    
    def setup_logging(self) -> None:
        """Setup logging configuration."""
        logging_config = self.get_logging_config()
        
        # Configure root logger
        logging.basicConfig(
            level=getattr(logging, logging_config.level.upper()),
            format=logging_config.format,
            handlers=[]
        )
        
        # Add console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(getattr(logging, logging_config.level.upper()))
        console_formatter = logging.Formatter(logging_config.format)
        console_handler.setFormatter(console_formatter)
        
        root_logger = logging.getLogger()
        root_logger.addHandler(console_handler)
        
        # Add file handler if specified
        if logging_config.file_path:
            try:
                from logging.handlers import RotatingFileHandler
                file_handler = RotatingFileHandler(
                    logging_config.file_path,
                    maxBytes=logging_config.max_file_size,
                    backupCount=logging_config.backup_count
                )
                file_handler.setLevel(getattr(logging, logging_config.level.upper()))
                file_handler.setFormatter(console_formatter)
                root_logger.addHandler(file_handler)
            except Exception as e:
                logging.warning(f"Failed to setup file logging: {e}")
        
        # Set specific logger levels
        logging.getLogger("uvicorn").setLevel(logging.INFO)
        logging.getLogger("fastapi").setLevel(logging.INFO)
        logging.getLogger("httpx").setLevel(logging.WARNING)
        
        if self.debug:
            logging.getLogger("app").setLevel(logging.DEBUG)
        
        logging.info("Logging configured successfully")


# Global settings instance
settings: Optional[Settings] = None


def get_settings() -> Settings:
    """Get or create the global settings instance."""
    global settings
    if settings is None:
        try:
            settings = Settings()
            settings.setup_logging()
        except Exception as e:
            # Fallback settings if environment variables are missing
            logging.error(f"Failed to load settings: {e}")
            # Create minimal settings for development
            os.environ.setdefault("OPENAI_API_KEY", "your-openai-key-here")
            os.environ.setdefault("SERPAPI_API_KEY", "your-serpapi-key-here")
            settings = Settings()
            settings.setup_logging()
    
    return settings


def load_environment_variables() -> None:
    """Load environment variables from .env file if it exists."""
    env_file = os.path.join(os.path.dirname(__file__), "..", "..", ".env")
    if os.path.exists(env_file):
        from dotenv import load_dotenv
        load_dotenv(env_file)
        logging.info(f"Loaded environment variables from {env_file}")
    else:
        logging.info("No .env file found, using system environment variables")


# Load environment variables on import
load_environment_variables()
