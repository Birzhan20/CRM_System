from pydantic import BaseModel
from decimal import Decimal


class AdCampaignBase(BaseModel):
    name: str
    service_id: int
    channel: str
    budget: Decimal

    class Config:
        from_attributes = True


class AdCampaignCreate(AdCampaignBase):
    pass


class AdCampaignUpdate(AdCampaignBase):
    pass


class AdCampaignDelete(AdCampaignBase):
    pass


class AdCampaignResponse(AdCampaignBase):
    id: int
