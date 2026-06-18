from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.db.engine import Base, engine

from app.api.v1.wallets import router as wallet_router
from app.api.v1.operations import router as operation_router
from app.api.v1.users import router as users_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield


app = FastAPI(lifespan=lifespan)

app.include_router(wallet_router, prefix='/api/v1', tags=['wallet'])
app.include_router(operation_router, prefix='/api/v1', tags=['operations'])
app.include_router(users_router, prefix='/api/v1', tags=['users'])
