from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from crud.users import require_role
from models.users import User
from schemas.ad_campaigns import AdCampaignUpdate, AdCampaignCreate, AdCampaignResponse
from crud.ad_campaigns import get_ad_campaigns, get_ad_campaign_by_id, get_ad_campaign_by_name, create_ad_campaign, \
    update_ad_campaign, delete_ad_campaign
from schemas.users import UserRole

router = APIRouter(prefix="/ad_campaigns", tags=["Ad_campaigns"])


@router.get('/', response_model=List[AdCampaignResponse], status_code=200)
async def ad_campaigns(db: AsyncSession = Depends(get_db),
                       current_user: User = Depends(require_role([UserRole.ADMIN, UserRole.MARKETER]))):
    return await get_ad_campaigns(db=db)


@router.get("/{ad_campaign_id}", response_model=AdCampaignResponse, status_code=200)
async def ad_campaign(ad_campaign_id: int, db: AsyncSession = Depends(get_db),
                      current_user: User = Depends(require_role([UserRole.ADMIN, UserRole.MARKETER]))):
    res = await get_ad_campaign_by_id(ad_campaign_id=ad_campaign_id, db=db)
    if not res:
        raise HTTPException(status_code=404, detail="AdCampaign not found")
    return res


@router.post("/", response_model=AdCampaignResponse, status_code=201)
async def create(ad_campaign: AdCampaignCreate, db: AsyncSession = Depends(get_db),
                 current_user: User = Depends(require_role([UserRole.ADMIN, UserRole.MARKETER]))):
    check = await get_ad_campaign_by_name(name=ad_campaign.name, db=db)
    if check:
        raise HTTPException(status_code=400, detail="AdCampaign already exists")
    res = await create_ad_campaign(ad_campaign=ad_campaign, db=db)
    return res


@router.put("/{ad_campaign_id}/", response_model=AdCampaignResponse, status_code=200)
async def update(ad_campaign_id: int, ad_campaing: AdCampaignUpdate, db: AsyncSession = Depends(get_db),
                 current_user: User = Depends(require_role([UserRole.ADMIN, UserRole.MARKETER]))):
    check = await get_ad_campaign_by_id(ad_campaign_id=ad_campaign_id, db=db)
    if check is None:
        raise HTTPException(status_code=404, detail="AdCampaign not found")
    res = await update_ad_campaign(ad_campaign=ad_campaing, db=db)
    return res


@router.delete("/{ad_campaign_id}/", response_model=AdCampaignResponse, status_code=200)
async def delete(ad_campaign_id: int, db: AsyncSession = Depends(get_db),
                 current_user: User = Depends(require_role([UserRole.ADMIN, UserRole.MARKETER]))):
    check = await get_ad_campaign_by_id(ad_campaign_id=ad_campaign_id, db=db)
    if check is None:
        raise HTTPException(status_code=404, detail="AdCampaign not found")
    res = await delete_ad_campaign(ad_campaign_id=ad_campaign_id, db=db)
    return res
