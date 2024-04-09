from contextlib import asynccontextmanager
from fastapi import FastAPI
from database import Base
from db_helper import db_helper
from items.router import router as items_router
from users.router import router as users_router

app = FastAPI()

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    

app.include_router(items_router)
app.include_router(users_router)

