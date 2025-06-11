from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from crud.users import require_role
from models.users import User
from schemas.services import ServiceCreate, ServiceUpdate, ServiceResponse
from crud.services import create_service, update_service, delete_service, get_service_by_name, get_service_by_id, \
    get_services
from schemas.users import UserRole

router = APIRouter(prefix="/services", tags=["Services"])


@router.get("/", response_model=List[ServiceResponse], status_code=200)
async def services(db: AsyncSession = Depends(get_db),
                   current_user: User = Depends(require_role([UserRole.ADMIN, UserRole.MARKETER]))):
    res = await get_services(db=db)
    return res


@router.get("/{service_id}", response_model=ServiceResponse, status_code=200)
async def get(service_id: int, db: AsyncSession = Depends(get_db),
              current_user: User = Depends(require_role([UserRole.ADMIN, UserRole.MARKETER]))):
    res = await get_service_by_id(id=service_id, db=db)
    if not res:
        raise HTTPException(status_code=404, detail="Service not found")
    return res


@router.post("/", response_model=ServiceResponse, status_code=201)
async def create(service: ServiceCreate, db: AsyncSession = Depends(get_db),
                 current_user: User = Depends(require_role([UserRole.ADMIN, UserRole.MARKETER]))):
    check = await get_service_by_name(name=service.name, db=db)
    if check:
        raise HTTPException(status_code=400, detail="Service already exists")
    res = await create_service(db=db, service=service)
    return res


@router.put("/{service_id}", response_model=ServiceResponse, status_code=200)
async def update(service_id: int, service: ServiceUpdate, db: AsyncSession = Depends(get_db),
                 current_user: User = Depends(require_role([UserRole.ADMIN, UserRole.MARKETER]))):
    check = await get_service_by_id(id=service_id, db=db)
    if not check:
        raise HTTPException(status_code=404, detail="Service not found")
    res = await update_service(service_id=service_id, service=service, db=db)
    return res


@router.delete("/{service_id}", response_model=dict, status_code=200)
async def delete(service_id: int, db: AsyncSession = Depends(get_db),
                 current_user: User = Depends(require_role([UserRole.ADMIN, UserRole.MARKETER]))):
    check = await get_service_by_id(id=service_id, db=db)
    if not check:
        raise HTTPException(status_code=404, detail="Service not found")
    await delete_service(service_id=service_id, db=db)
    return {"detail": "Service deleted"}
