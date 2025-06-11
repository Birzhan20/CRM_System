from pydantic import BaseModel, EmailStr, field_validator
import phonenumbers


class ClientBase(BaseModel):
    full_name: str
    phone: str
    email: EmailStr
    ad_campaign_id: int | None

    @field_validator('phone')
    def validate_phone(cls, value):
        try:
            parsed_number = phonenumbers.parse(value, None)
            if not phonenumbers.is_valid_number(parsed_number):
                raise ValueError('Invalid phone number')
            return phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)
        except Exception:
            raise ValueError('Invalid phone number format')

    class Config:
        from_attributes = True


class ClientCreate(ClientBase):
    pass

class ClientUpdate(ClientBase):
    is_active: bool

class ClientDelete(ClientBase):
    pass

class ClientResponse(ClientBase):
    id: int
