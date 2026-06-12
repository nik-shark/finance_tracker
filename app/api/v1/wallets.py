from fastapi import APIRouter

from app.schemas import CreateWalletRequest
from app.service import wallets as wallet_service

router = APIRouter()


# передача черезе querry params
@router.get('/balance')
def get_balance(wallet_name: str | None = None):
    return wallet_service.get_balance(wallet_name)


# path-params
@router.post('/wallets')
def create_wallet(wallet: CreateWalletRequest):
    return wallet_service.create_wallet(wallet)