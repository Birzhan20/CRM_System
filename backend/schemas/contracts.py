from decimal import Decimal
from datetime import date
from pydantic import BaseModel


class ContractsBase(BaseModel):
    name: str
    service_id: int
    client_id: int
    document_file: str
    conclusion_date: date
    duration: date | None
    amount: Decimal

    class Config:
        from_attributes = True


class ContractsCreate(ContractsBase):
    pass


class ContractsUpdate(ContractsBase):
    pass


class ContractsDelete(ContractsBase):
    pass


class ContractResponse(ContractsBase):
    id: int
