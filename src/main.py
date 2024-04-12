from contextlib import asynccontextmanager
from fastapi import FastAPI
from items.router import router as items_router
from users.router import router as users_router
from products.router import router as products_router

app = FastAPI()

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    

app.include_router(items_router)
app.include_router(users_router)
app.include_router(products_router)

