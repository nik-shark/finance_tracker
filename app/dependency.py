from fastapi import HTTPException
from fastapi.params import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.engine import AsyncSessionLocal
from app.db.models import User
from app.repository import users as users_repository

# TODO нужно реализовать нормальный JWT
security = HTTPBearer()


async def get_db():
    async with AsyncSessionLocal() as db:
        yield db


async def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(security),
        db: AsyncSession = Depends(get_db)
) -> User:

    login = credentials.credentials

    user = await users_repository.get_user(db, login)

    if not user:
        raise HTTPException(status_code=401, detail='Unauthorized')

    return user
