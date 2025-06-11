from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from crud.users import require_role
from models.users import User
from schemas.clients import ClientCreate, ClientUpdate, ClientResponse
from crud.clients import create_client, update_client, delete_client, get_clients, get_client_by_id, get_client_by_phone
from schemas.users import UserRole

router = APIRouter(prefix="/clients", tags=["Clients"])


@router.get("/", response_model=List[ClientResponse], status_code=200)
async def clients(db: AsyncSession = Depends(get_db),
                  current_user: User = Depends(require_role([UserRole.ADMIN, UserRole.OPERATOR]))):
    res = await get_clients(db=db)
    return res


@router.get("/{client_id}", response_model=ClientResponse, status_code=200)
async def client(client_id: int, db: AsyncSession = Depends(get_db),
                 current_user: User = Depends(require_role([UserRole.ADMIN, UserRole.OPERATOR]))):
    res = await get_client_by_id(client_id=client_id, db=db)
    if res is None:
        raise HTTPException(status_code=404, detail="Client not found")
    return res


@router.post("/", response_model=ClientResponse, status_code=201)
async def create(client: ClientCreate, db: AsyncSession = Depends(get_db),
                 current_user: User = Depends(require_role([UserRole.ADMIN, UserRole.OPERATOR]))):
    check = await get_client_by_phone(phone=client.phone, db=db)
    if check:
        raise HTTPException(status_code=400, detail="Client already exists")
    res = await create_client(client=client, db=db)
    return res


@router.post("/{client_id}", response_model=ClientResponse, status_code=200)
async def update(client_id: int, client: ClientUpdate, db: AsyncSession = Depends(get_db),
                 current_user: User = Depends(require_role([UserRole.ADMIN, UserRole.OPERATOR]))):
    check = await get_client_by_id(client_id=client_id, db=db)
    if check is None:
        raise HTTPException(status_code=404, detail="Client not found")
    res = await update_client(client_id=client_id, client=client, db=db)
    return res


@router.delete("/{client_id}", response_model=dict, status_code=200)
async def delete(client_id: int, db: AsyncSession = Depends(get_db),
                 current_user: User = Depends(require_role([UserRole.ADMIN, UserRole.OPERATOR]))):
    check = await get_client_by_id(client_id=client_id, db=db)
    if check is None:
        raise HTTPException(status_code=404, detail="Client not found")
    await delete_client(client_id=client_id, db=db)
    return {"detail": "Client deleted"}
