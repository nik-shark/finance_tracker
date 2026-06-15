from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Wallet

async def is_wallet_exist(wallet_name: str, db: AsyncSession) -> bool:

    result = await db.execute(
        select(Wallet).where(
            Wallet.name == wallet_name
        )
    )

    wallet = result.scalar_one_or_none()

    return wallet is not None


async def add_income(wallet_name: str, amount: float, db: AsyncSession) -> Wallet:

    result = await db.execute(
        select(Wallet).where(
            Wallet.name == wallet_name
        )
    )

    wallet = result.scalar_one_or_none()

    wallet.balance += Decimal(str(amount))

    await db.commit()
    await db.refresh(wallet)

    return wallet


async def get_wallet_balance_by_name(wallet_name: str, db: AsyncSession) -> Wallet:

    result = await db.execute(
        select(Wallet).where(
            Wallet.name == wallet_name
        )
    )

    return result.scalar_one_or_none()


async def add_expense(wallet_name: str, amount: float, db: AsyncSession) -> Wallet:

    result = await db.execute(
        select(Wallet).where(
            Wallet.name == wallet_name
        )
    )

    wallet = result.scalar_one_or_none()

    wallet.balance -= Decimal(str(amount))

    await db.commit()
    await db.refresh(wallet)

    return wallet


async def get_all_wallets(db: AsyncSession) -> list[Wallet]:
    result = await db.execute(select(Wallet))

    return result.scalars().all()


async def create_wallet(wallet_name: str, amount: float, db: AsyncSession) -> Wallet:

    wallet = Wallet(name=wallet_name, balance=amount)

    db.add(wallet)

    await db.commit()
    await db.refresh(wallet)

    return wallet