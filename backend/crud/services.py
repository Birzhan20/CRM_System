from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from models.services import Service
from schemas.services import ServiceCreate, ServiceUpdate, ServiceDelete, ServiceUpdate


async def get_service_by_name(name: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Service).filter(Service.name == name))
    return result.scalars().one_or_none()


async def get_service_by_id(id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Service).filter(Service.id == id))
    return result.scalars().one_or_none()


async def get_services(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Service).offset(skip).limit(limit))
    return result.scalars().all()


async def create_service(service: ServiceCreate, db: AsyncSession = Depends(get_db)):
    db_service = Service(**service.model_dump())
    db.add(db_service)
    await db.commit()
    await db.refresh(db_service)
    return db_service


async def update_service(service_id: int, service: ServiceUpdate, db: AsyncSession = Depends(get_db)):
    res = await get_service_by_id(service_id, db=db)
    for key, value in service.model_dump(exclude_unset=True).items():
        setattr(res, key, value)
    await db.commit()
    await db.refresh(res)
    return res


async def delete_service(service_id: int, db: AsyncSession = Depends(get_db)):
    res = await get_service_by_id(service_id, db=db)
    await db.delete(res)
    await db.commit()
    return
