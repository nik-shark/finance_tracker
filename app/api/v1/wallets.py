from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import CreateWalletRequest
from app.service import wallets as wallet_service
from app.db.engine import get_db

router = APIRouter()


# передача черезе querry params
@router.get('/balance')
async def get_balance(
        db: AsyncSession = Depends(get_db),
        wallet_name: str | None = None
):

    return await wallet_service.get_wallet(db, wallet_name)


# path-params
@router.post('/wallets')
async def create_wallet(
        wallet: CreateWalletRequest,
        db: AsyncSession = Depends(get_db)
):

    return await wallet_service.create_wallet(wallet, db)
