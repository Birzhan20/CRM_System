from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from models.clients import Client
from schemas.clients import ClientCreate, ClientUpdate


async def get_clients(skip: int = 0, limit: int = 20, db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(Client).offset(skip).limit(limit))
    return res.scalars().all()


async def get_client_by_id(client_id: int, db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(Client).where(Client.id == client_id))
    return res.scalars().one_or_none()


async def get_client_by_phone(phone: str, db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(Client).where(Client.phone == phone))
    return res.scalars().one_or_none()


async def create_client(client: ClientCreate, db: AsyncSession = Depends(get_db)):
    db_client = Client(**client.model_dump())
    db.add(db_client)
    await db.commit()
    await db.refresh(db_client)
    return db_client


async def update_client(client_id: int, client: ClientUpdate, db: AsyncSession = Depends(get_db)):
    res = await get_client_by_id(client_id=client_id, db=db)
    for key, value in client.model_dump(exclude_unset=True).items():
        setattr(res, key, value)
    await db.commit()
    await db.refresh(res)
    return res


async def delete_client(client_id: int, db: AsyncSession = Depends(get_db)):
    res = await get_client_by_id(client_id=client_id, db=db)
    await db.delete(res)
    await db.commit()
    return