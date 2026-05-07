from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import List, Optional

class Settings(BaseSettings):
    # App
    APP_NAME: str = "ProductIntel"
    ENVIRONMENT: str = "development"
    DEBUG: bool = False
    
    # Database
    DATABASE_URL: str = "postgresql+asyncpg://app:devpassword@localhost:5432/product_intel"
    DATABASE_URL_SYNC: str = "postgresql://app:devpassword@localhost:5432/product_intel"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # Auth
    JWT_SECRET: str = "change-me-in-production"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30
    
    # MiniMax M2.7
    MINIMAX_API_KEY: str = ""
    MINIMAX_GROUP_ID: str = ""
    MINIMAX_BASE_URL: str = "https://api.minimaxi.chat/v1"
    MINIMAX_MODEL: str = "MiniMax-M2.7"
    MINIMAX_MAX_TOKENS: int = 4096
    MINIMAX_TEMPERATURE: float = 0.1
    MINIMAX_TOP_P: float = 0.9
    MINIMAX_TIMEOUT_SECONDS: int = 60
    MINIMAX_MAX_RETRIES: int = 3
    
    # Facebook Ad Library
    FB_ACCESS_TOKEN: str = ""
    FB_API_VERSION: str = "v19.0"
    FB_RATE_LIMIT_PER_HOUR: int = 200
    FB_TOKEN_POOL_MIN_SIZE: int = 2
    
    # Scraping / Proxy
    BRIGHT_DATA_USER: Optional[str] = None
    BRIGHT_DATA_PASS: Optional[str] = None
    BRIGHT_DATA_PROXY: str = "http://brd.superproxy.io:22225"
    PLAYWRIGHT_HEADLESS: bool = True
    
    # Amazon PA API 5.0
    AMAZON_PA_API_KEY: str = ""
    AMAZON_PA_API_SECRET: str = ""
    AMAZON_ASSOCIATE_TAG: str = ""
    AMAZON_REGION: str = "us-east-1"
    
    # Stripe
    STRIPE_SECRET_KEY: Optional[str] = None
    STRIPE_WEBHOOK_SECRET: Optional[str] = None
    STRIPE_PUBLISHABLE_KEY: Optional[str] = None
    
    # Plans & Quotas
    PLAN_LIMITS: dict = {
        "starter": {"daily_analyses": 50, "watchlist_items": 10, "exports": 5},
        "pro": {"daily_analyses": 500, "watchlist_items": 100, "exports": 50},
        "agency": {"daily_analyses": 5000, "watchlist_items": 1000, "exports": 500},
    }
    
    # Rate Limiting
    RATE_LIMIT_IP_PER_MINUTE: int = 100
    RATE_LIMIT_USER_CONCURRENT_ANALYSES: int = 3
    
    # Cache TTLs (seconds)
    CACHE_TTL_FB_ADS: int = 21600       # 6 hours
    CACHE_TTL_ALIBABA: int = 43200      # 12 hours
    CACHE_TTL_AMAZON: int = 86400       # 24 hours
    CACHE_TTL_GOOGLE_TRENDS: int = 43200 # 12 hours
    
    # Circuit Breaker
    CIRCUIT_FAILURE_THRESHOLD: int = 5
    CIRCUIT_RECOVERY_TIMEOUT: int = 300  # 5 minutes
    
    # Notifications
    RESEND_API_KEY: Optional[str] = None
    FROM_EMAIL: str = "alerts@productintel.io"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    return Settings()
