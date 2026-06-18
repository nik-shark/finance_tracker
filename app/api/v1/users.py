from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import User
from app.schemas import UserRequest, UserResponse
from app.service import users as users_service
from app.dependency import get_db, get_current_user

router = APIRouter()


@router.post('/users', response_model=UserResponse)
async def create_user(
        payload: UserRequest,
        db: AsyncSession = Depends(get_db)
):
    return await users_service.create_user(db, payload.login)


@router.post('/users/me', response_model=UserResponse)
async def get_current_user(current_user: User = Depends(get_current_user)):
    return UserResponse.model_validate(current_user)
