from os import getenv
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    db_url: str = f'postgresql+asyncpg://home:123@localhost:5432/shop_fastapi_test_cource'
    db_echo: bool = True

settings = Settings()

