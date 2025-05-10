from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    openai_api_key: str  # ← This must be declared!

    class Config:
        env_file = ".env"
