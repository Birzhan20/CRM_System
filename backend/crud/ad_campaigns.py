from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from models.ad_campaigns import AdCampaign
from schemas.ad_campaigns import AdCampaignUpdate, AdCampaignCreate, AdCampaignUpdate


async def get_ad_campaigns(skip: int = 0, limit: int = 20, db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(AdCampaign).offset(skip).limit(limit))
    return res.scalars().all()


async def get_ad_campaign_by_id(ad_campaign_id: int, db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(AdCampaign).filter(AdCampaign.id == ad_campaign_id))
    return res.scalars().one_or_none()


async def get_ad_campaign_by_name(name: str, db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(AdCampaign).filter(AdCampaign.name == name))
    return res.scalars().one_or_none()


async def create_ad_campaign(ad_campaign: AdCampaignCreate, db: AsyncSession = Depends(get_db)):
    db_ad_campaign = AdCampaign(**ad_campaign.model_dump())
    db.add(db_ad_campaign)
    await db.commit()
    await db.refresh(db_ad_campaign)
    return db_ad_campaign


async def update_ad_campaign(ad_campaign: AdCampaignUpdate, db: AsyncSession = Depends(get_db)):
    for key, value in ad_campaign.model_dump().items():
        setattr(ad_campaign, key, value)
    await db.commit()
    await db.refresh(ad_campaign)
    return ad_campaign


async def delete_ad_campaign(ad_campaign_id: int, db: AsyncSession = Depends(get_db)):
    res = await db.delete(ad_campaign_id)
    await db.commit()
    await db.refresh(res)
    return
