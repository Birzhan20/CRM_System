from decimal import Decimal

from pydantic import BaseModel


class ServiceBase(BaseModel):
    name: str
    description: str
    price: Decimal

    class Config:
        from_attributes = True


class ServiceCreate(ServiceBase):
    pass


class ServiceUpdate(ServiceBase):
    pass


class ServiceDelete(ServiceBase):
    pass


class ServiceResponse(ServiceBase):
    id: int
