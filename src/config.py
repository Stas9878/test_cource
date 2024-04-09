from os import getenv
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    db_url: str = f'postgresql+asyncpg://user:password@host:port/dbname'
    db_echo: bool = True

settings = Settings()

