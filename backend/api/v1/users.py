from typing import List

from fastapi import HTTPException, APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from crud.users import create_user, get_user_by_email, read_users, read_user, update_user, \
    delete_user, require_role
from models.users import User
from schemas.users import UserResponse, UserCreate, UserUpdate, UserRole

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=UserResponse, status_code=201)
async def create(user: UserCreate, db: AsyncSession = Depends(get_db)):
    check = await get_user_by_email(email=str(user.email), db=db)
    if check:
        raise HTTPException(status_code=400, detail="Email already registered")
    res = await create_user(user, db)
    return res


@router.get("/", response_model=List[UserResponse], status_code=200)
async def users(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db),
                current_user: User = Depends(require_role([UserRole.ADMIN]))):
    res = await read_users(skip=skip, limit=limit, db=db)
    return res


@router.get("/{user_id}", response_model=UserResponse, status_code=200)
async def user(user_id: int, db: AsyncSession = Depends(get_db),
               current_user: User = Depends(require_role([UserRole.ADMIN]))):
    res = await read_user(user_id=user_id, db=db)
    return res


@router.put("/{user_id}", response_model=UserResponse, status_code=200)
async def update(user_id: int, user: UserUpdate, db: AsyncSession = Depends(get_db),
                 current_user: User = Depends(require_role([UserRole.ADMIN]))):
    check = await read_user(user_id=user_id, db=db)
    if not check:
        raise HTTPException(status_code=404, detail="User not found")
    res = await update_user(user_id=user_id, user=user, db=db)
    return res


@router.delete("/{user_id}", response_model=dict, status_code=200)
async def delete(user_id: int, db: AsyncSession = Depends(get_db),
                 current_user: User = Depends(require_role([UserRole.ADMIN]))):
    check = await read_user(user_id=user_id, db=db)
    if not check:
        raise HTTPException(status_code=404, detail="User not found")
    await delete_user(user_id, db=db)
    return {"detail": "User deleted"}
