from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from pydantic import BaseModel
import os


load_dotenv()

DB_USER = os.environ.get('DB_USER')
DB_NAME = os.environ.get('DB_NAME')
DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
DB_PASSWORD = os.environ.get('DB_PASSWORD')


class DBSettings(BaseModel):
    url: str = f'postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    echo: bool = False


class Settings(BaseSettings):
    db: DBSettings = DBSettings()
    

settings = Settings()

