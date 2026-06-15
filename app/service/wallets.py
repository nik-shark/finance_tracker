from fastapi import HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.repository import wallets as wallets_repository
from app.schemas import CreateWalletRequest


async def get_wallet(
        db: AsyncSession,
        wallet_name: str | None = None
):

    if wallet_name is None:
        wallets = await wallets_repository.get_all_wallets(db)
        return {'total_balance': sum([w.balance for w in wallets])}

    if not await wallets_repository.is_wallet_exist(wallet_name, db):
        raise HTTPException(
            status_code=404,
            detail=f'Wallet {wallet_name} not found',
        )

    wallet = await wallets_repository.get_wallet_balance_by_name(wallet_name, db)

    return {
        'wallet': wallet.name,
        'balance': wallet.balance
    }


async def create_wallet(wallet: CreateWalletRequest, db: AsyncSession):

    if await wallets_repository.is_wallet_exist(wallet.name, db):
        raise HTTPException(
            status_code=400,
            detail=f'Wallet {wallet.name} already exists',
        )

    new_wallet = await wallets_repository.create_wallet(
        wallet.name,
        wallet.initial_balance,
        db
    )

    return {
        'message': f'Wallet {wallet.name} created',
        'wallet': wallet.name,
        'balance': new_wallet.balance,
    }
