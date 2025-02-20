# app/config.py
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    groq_api_key: str
    audio_upload_dir: str = "app/static/audio"
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()