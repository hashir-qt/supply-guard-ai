from openai import AsyncOpenAI
from backend.config import get_settings

settings = get_settings()

def get_openai_client() -> AsyncOpenAI:
    return AsyncOpenAI(
        api_key=settings.OPENAI_API_KEY,
        base_url="https://api.openai.com/v1"
    )
