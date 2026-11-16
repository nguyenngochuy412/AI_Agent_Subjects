from contextlib import asynccontextmanager

from fastapi import FastAPI

from app import models
from app.api.chat import router as chat_router
from app.core.config import settings
from app.db.session import Base, engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()

app = FastAPI(title=settings.app_name, lifespan=lifespan)

@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}

app.include_router(chat_router)