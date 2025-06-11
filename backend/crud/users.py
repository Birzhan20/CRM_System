from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from core.utils import decode_token, hash_password
from models.users import User
from schemas.users import UserCreate, UserUpdate, UserRole

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)) ->User:
    payload = decode_token(token)
    if payload is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    email: str = payload.get("sub")
    if email is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    res = await db.execute(select(User).filter(User.email == email))
    user = res.scalars().one_or_none()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user


def require_role(allowed_roles: list[UserRole]):
    async def check_role(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to perform this action"
            )
        return current_user
    return check_role


async def get_user_by_email(email: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).filter(User.email == email))
    return result.scalars().one_or_none()


async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    hashed_password = hash_password(user.password_hash)
    db_user = User(
        first_name = user.first_name,
        last_name = user.last_name,
        password_hash = hashed_password,
        email = str(user.email),
        phone = str(user.phone),
        role = user.role,
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def read_users(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).offset(skip).limit(limit))
    return result.scalars().all()


async def read_user(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).filter(User.id == user_id))
    user = result.scalars().one_or_none()
    return user


async def update_user(user_id: int, user: UserUpdate, db: AsyncSession):
    db_user = await read_user(user_id=user_id, db=db)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    update_data = user.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        if key == "password_hash" and value:
            value = hash_password(value)
        setattr(db_user, key, value)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    res = await read_user(user_id=user_id, db=db)
    await db.delete(res)
    await db.commit()
    return
