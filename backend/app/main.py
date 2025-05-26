from fastapi import FastAPI
from app.api.v1 import api_router
from app.db.database import check_db_connected, check_db_disconnected
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    await check_db_connected()
    yield
    await check_db_disconnected()


# Dependency for DB session
app = FastAPI(lifespan=lifespan)

app.include_router(api_router, prefix="/api/v1")
