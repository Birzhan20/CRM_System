from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from crud.users import require_role
from models.users import User
from schemas.contracts import ContractsUpdate, ContractsCreate, ContractResponse
from crud.contracts import create_contract, update_contract, delete_contract, get_contracts, get_contracts_by_id, \
    get_contracts_by_name
from schemas.users import UserRole

router = APIRouter(prefix="/contracts", tags=["Contracts"])


@router.get("/", response_model=List[ContractResponse], status_code=200)
async def contracts(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db),
                    current_user: User = Depends(require_role([UserRole.ADMIN, UserRole.MANAGER]))):
    res = await get_contracts(skip=skip, limit=limit, db=db)
    return res


@router.get("/{contract_id}", response_model=ContractResponse, status_code=200)
async def contract(contract_id: int, db: AsyncSession = Depends(get_db),
                   current_user: User = Depends(require_role([UserRole.ADMIN, UserRole.MARKETER]))):
    res = await get_contracts_by_id(id=contract_id, db=db)
    if not res:
        raise HTTPException(status_code=404, detail="Contract not found")
    return res


@router.post("/", response_model=ContractResponse, status_code=201)
async def create(contract: ContractsCreate, db: AsyncSession = Depends(get_db),
                 current_user: User = Depends(require_role([UserRole.ADMIN, UserRole.MARKETER]))):
    check = await get_contracts_by_name(name=contract.name, db=db)
    if check:
        raise HTTPException(status_code=400, detail="Contract already exists")
    res = await create_contract(contract=contract, db=db)
    return res


@router.put("/{contract_id}", response_model=ContractResponse, status_code=200)
async def update(contract_id: int, contract: ContractsUpdate, db: AsyncSession = Depends(get_db),
                 current_user: User = Depends(require_role([UserRole.ADMIN, UserRole.MARKETER]))):
    check = await get_contracts_by_id(id=contract_id, db=db)
    if not check:
        raise HTTPException(status_code=404, detail="Contract not found")
    res = await update_contract(contract_id=contract_id, contract=contract, db=db)
    return res


@router.delete("/{contract_id}", response_model=dict, status_code=200)
async def delete(contract_id: int, db: AsyncSession = Depends(get_db),
                 current_user: User = Depends(require_role([UserRole.ADMIN, UserRole.MARKETER]))):
    check = await get_contracts_by_id(id=contract_id, db=db)
    if not check:
        raise HTTPException(status_code=404, detail="Contract not found")
    res = await delete_contract(contract_id=contract_id, db=db)
    return {'detail': 'Contract deleted'}
