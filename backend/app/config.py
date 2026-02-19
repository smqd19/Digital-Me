from pydantic_settings import BaseSettings
from functools import lru_cache
import os
import json


class Settings(BaseSettings):
    openai_api_key: str = ""
    model_name: str = "gpt-4o-mini"
    embedding_model: str = "text-embedding-3-small"
    chroma_persist_directory: str = "./data/chroma_db"
    knowledge_base_path: str = "./data/knowledge_base.json"
    
    # CORS settings - accepts JSON string or list
    cors_origins: list[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Handle CORS_ORIGINS as JSON string from environment
        cors_env = os.getenv("CORS_ORIGINS")
        if cors_env:
            try:
                self.cors_origins = json.loads(cors_env)
            except json.JSONDecodeError:
                # If it's comma-separated, split it
                self.cors_origins = [o.strip() for o in cors_env.split(",")]


@lru_cache()
def get_settings() -> Settings:
    return Settings()
