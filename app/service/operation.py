from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import OperationRequest
from app.repository import wallets as wallets_repository


async def add_income(
        operations: OperationRequest,
        db: AsyncSession
):

    if not await wallets_repository.is_wallet_exist(operations.wallet_name, db):
        raise HTTPException(
            status_code=404,
            detail=f'Wallet {operations.wallet_name} not found',
        )

    wallet = await wallets_repository.add_income(
        operations.wallet_name,
        operations.amount,
        db
    )

    return {
        'message': 'Income added',
        'wallet': operations.wallet_name,
        'amount': operations.amount,
        'descriptions': operations.description,
        'new_balance': wallet.balance,
    }


async def add_expense(
        operations: OperationRequest,
        db: AsyncSession
):

    if not await wallets_repository.is_wallet_exist(operations.wallet_name, db):
        raise HTTPException(
            status_code=404,
            detail=f'Wallet {operations.wallet_name} not found',
        )

    wallet = await wallets_repository.get_wallet_balance_by_name(operations.wallet_name, db)
    if wallet.balance < operations.amount:
        raise HTTPException(
            status_code=400,
            detail=f'Insufficient funds. '
                   f'Available: {wallet.balance}',

        )

    wallet = await wallets_repository.add_expense(
        operations.wallet_name,
        operations.amount,
        db)

    return {
        'message': 'Expense added',
        'wallet': operations.wallet_name,
        'amount': operations.amount,
        'descriptions': operations.description,
        'new_balance': wallet.balance,
    }