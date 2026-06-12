from fastapi import HTTPException

from app.schemas import OperationRequest
from app.repository import wallets as wallets_repository


def add_income(operations: OperationRequest):

    if wallets_repository.is_wallet_exist(operations.wallet_name):
        raise HTTPException(
            status_code=404,
            detail=f'Wallet {operations.wallet_name} not found',
        )

    new_balance = wallets_repository.add_income(
        operations.wallet_name,
        operations.amount
    )

    return {
        'message': 'Income added',
        'wallet': operations.wallet_name,
        'amount': operations.amount,
        'descriptions': operations.description,
        'new_balance': new_balance,
    }


def add_expense(operations: OperationRequest):

    if not wallets_repository.is_wallet_exist(operations.wallet_name):
        raise HTTPException(
            status_code=404,
            detail=f'Wallet {operations.wallet_name} not found',
        )

    balance = wallets_repository.get_wallet_balance_by_name(operations.wallet_name)
    if balance < operations.amount:
        raise HTTPException(
            status_code=400,
            detail=f'Insufficient funds. '
                   f'Available: {balance}',

        )

    new_balance = wallets_repository.add_expense(operations.wallet_name)

    return {
        'message': 'Expense added',
        'wallet': operations.wallet_name,
        'amount': operations.amount,
        'descriptions': operations.description,
        'new_balance': new_balance,
    }