import enum
from pydantic import BaseModel, EmailStr


class UserRole(str, enum.Enum):
    ADMIN = "Administrator"
    OPERATOR = "Operator"
    MARKETER = "Marketer"
    MANAGER = "Manager"


class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    role: UserRole

    class Config:
        from_attributes = True


class UserCreate(UserBase):
    password_hash: str


class UserUpdate(UserBase):
    pass


class UserDelete(UserBase):
    pass


class UserResponse(UserBase):
    id: int
