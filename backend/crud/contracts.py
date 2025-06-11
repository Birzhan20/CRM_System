from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from models.contracts import Contract
from schemas.contracts import ContractsCreate, ContractsUpdate, ContractsDelete


async def get_contracts(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(Contract).offset(skip).limit(limit))
    return res.scalars().all()


async def get_contracts_by_name(name: str, db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(Contract).filter(Contract.name == name))
    return res.scalars().one_or_none()


async def get_contracts_by_id(id: int, db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(Contract).filter(Contract.id == id))
    return res.scalars().one_or_none()


async def create_contract(contract: ContractsCreate, db: AsyncSession = Depends(get_db)):
    db_contract = Contract(**contract.model_dump())
    db.add(db_contract)
    await db.commit()
    await db.refresh(db_contract)
    return db_contract


async def update_contract(contract_id: int, contract: ContractsUpdate, db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(Contract).filter(Contract.id == contract_id))
    db_contract = res.scalars().one_or_none()
    if not res:
        raise HTTPException(status_code=404, detail="Contract not found")
    for key, value in contract.model_dump(exclude_unset=True).items():
        setattr(db_contract, key, value)
    await db.commit()
    await db.refresh(db_contract)
    return db_contract


async def delete_contract(contract_id: int, db: AsyncSession = Depends(get_db)):
    res = await get_contracts_by_id(contract_id, db=db)
    await db.delete(res)
    await db.commit()
    return
