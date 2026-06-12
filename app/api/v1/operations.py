from fastapi import APIRouter

from app.schemas import OperationRequest
from app.service import operation as operations_service

router = APIRouter()


@router.post('/operations/income')
def add_income(operations: OperationRequest):
    return operations_service.add_income(operations)


@router.post('/operations/expense')
def add_expense(operations: OperationRequest):
    return operations_service.add_expense(operations)
