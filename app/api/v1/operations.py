from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends

from app.db.models import User
from app.schemas import OperationRequest
from app.service import operation as operations_service
from app.dependency import get_db, get_current_user

router = APIRouter()


@router.post('/operations/income')
async def add_income(
        operations: OperationRequest,
        db:AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):

    return await operations_service.add_income(operations, current_user, db)


@router.post('/operations/expense')
async def add_expense(
        operations: OperationRequest,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):

    return await operations_service.add_expense(operations, current_user, db)
