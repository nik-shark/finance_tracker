from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends

from app.schemas import OperationRequest
from app.service import operation as operations_service
from app.db.engine import get_db

router = APIRouter()


@router.post('/operations/income')
async def add_income(
        operations: OperationRequest,
        db:AsyncSession = Depends(get_db)
):

    return await operations_service.add_income(operations, db)


@router.post('/operations/expense')
async def add_expense(
        operations: OperationRequest,
        db: AsyncSession = Depends(get_db)
):

    return await operations_service.add_expense(operations, db)
