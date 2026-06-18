from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Wallet, User


async def is_wallet_exist(wallet_name: str, user_id: int, db: AsyncSession) -> bool:

    result = await db.execute(
        select(Wallet).where(
            Wallet.name == wallet_name,
            Wallet.user_id == user_id
        )
    )

    wallet = result.scalar_one_or_none()

    return wallet is not None


async def add_income(
        wallet_name: str,
        amount: float,
        user_id: int,
        db: AsyncSession
) -> Wallet:

    result = await db.execute(
        select(Wallet).where(
            Wallet.name == wallet_name,
            Wallet.user_id == user_id
        )
    )

    wallet = result.scalar_one_or_none()

    wallet.balance += Decimal(str(amount))

    await db.commit()
    await db.refresh(wallet)

    return wallet


async def get_wallet_balance_by_name(
        wallet_name: str,
        user_id: int,
        db: AsyncSession) -> Wallet:

    result = await db.execute(
        select(Wallet).where(
            Wallet.name == wallet_name,
            Wallet.user_id == user_id
        )
    )

    return result.scalar_one_or_none()


async def add_expense(
        wallet_name: str,
        amount: float,
        user_id: int,
        db: AsyncSession) -> Wallet:

    result = await db.execute(
        select(Wallet).where(
            Wallet.name == wallet_name,
            Wallet.user_id == user_id
        )
    )

    wallet = result.scalar_one_or_none()

    wallet.balance -= Decimal(str(amount))

    await db.commit()
    await db.refresh(wallet)

    return wallet


async def get_all_wallets(
        db: AsyncSession,
        user_id: int
) -> list[Wallet]:

    result = await db.execute(
        select(Wallet).where(
            User.id == user_id,
            Wallet.user_id == user_id
        )
    )

    return result.scalars().all()


async def create_wallet(
        wallet_name: str,
        amount: float,
        user_id: int,
        db: AsyncSession
) -> Wallet:

    wallet = Wallet(name=wallet_name, balance=amount, user_id=user_id)

    db.add(wallet)

    await db.commit()
    await db.refresh(wallet)

    return wallet