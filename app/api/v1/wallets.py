from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.users import get_current_user
from app.db.models import User
from app.schemas import CreateWalletRequest
from app.service import wallets as wallet_service
from app.dependency import get_db

router = APIRouter()


@router.get('/balance')
async def get_balance(
        db: AsyncSession = Depends(get_db),
        wallet_name: str | None = None,
        current_user: User = Depends(get_current_user)
):

    return await wallet_service.get_wallet(db, current_user, wallet_name)


@router.post('/wallets')
async def create_wallet(
        wallet: CreateWalletRequest,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):

    return await wallet_service.create_wallet(wallet, current_user, db)
