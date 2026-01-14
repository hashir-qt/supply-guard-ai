from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )
    
    API_V1_PREFIX: str = "/api"
    DEBUG: bool = True
    
    # OpenAI - Direct API Key
    OPENAI_API_KEY: str
    OPENAI_MODEL: str = "gpt-4o-mini"
    
    # Neon PostgreSQL Database
    DATABASE_URL: str
    

@lru_cache()
def get_settings():
    return Settings()
