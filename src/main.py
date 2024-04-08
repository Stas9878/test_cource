from fastapi import FastAPI
from items.router import router as items_router
from users.router import router as users_router

app = FastAPI()

app.include_router(items_router)
app.include_router(users_router)

