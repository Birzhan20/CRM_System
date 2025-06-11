from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select, Integer
from typing import List, Dict, Optional
from models.ad_campaigns import AdCampaign
from models.clients import Client
from models.contracts import Contract

async def get_campaign_stats(db: AsyncSession) -> List[Dict]:
    """
    Получение статистики по всем рекламным кампаниям.
    Возвращает список словарей с данными о кампаниях.
    """
    query = (
        select(
            AdCampaign.id,
            AdCampaign.name,
            AdCampaign.budget,
            func.count(Client.id).label("total_clients"),
            func.sum(Client.is_active.cast(Integer)).label("active_clients"),
            func.coalesce(func.sum(Contract.amount), 0).label("total_revenue")
        )
        .outerjoin(Client, AdCampaign.id == Client.ad_campaign_id)
        .outerjoin(Contract, Client.id == Contract.client_id)
        .group_by(AdCampaign.id, AdCampaign.name, AdCampaign.budget)
    )

    result = await db.execute(query)
    stats = result.all()

    result_list = []
    for stat in stats:
        total_clients = stat.total_clients or 0
        active_clients = stat.active_clients or 0
        total_revenue = float(stat.total_revenue) if stat.total_revenue else 0.0
        budget = float(stat.budget) if stat.budget else 0.0

        # Рассчитываем соотношение дохода к расходам (ROI)
        roi = (total_revenue / budget * 100) if budget > 0 else 0.0

        result_list.append({
            "campaign_id": stat.id,
            "campaign_name": stat.name,
            "budget": budget,
            "total_clients": total_clients,
            "active_clients": active_clients,
            "potential_clients": total_clients - active_clients,
            "total_revenue": total_revenue,
            "roi_percentage": round(roi, 2)
        })

    return result_list


async def get_campaign_stats_by_id(db: AsyncSession, campaign_id: int) -> Optional[Dict]:
    """
    Получение статистики по конкретной рекламной кампании.
    """
    query = (
        select(
            AdCampaign.id,
            AdCampaign.name,
            AdCampaign.budget,
            func.count(Client.id).label("total_clients"),
            func.sum(Client.is_active.cast(Integer)).label("active_clients"),
            func.coalesce(func.sum(Contract.amount), 0).label("total_revenue")
        )
        .outerjoin(Client, AdCampaign.id == Client.ad_campaign_id)
        .outerjoin(Contract, Client.id == Contract.client_id)
        .filter(AdCampaign.id == campaign_id)
        .group_by(AdCampaign.id, AdCampaign.name, AdCampaign.budget)
    )

    result = await db.execute(query)
    stat = result.first()

    if not stat:
        return None

    total_clients = stat.total_clients or 0
    active_clients = stat.active_clients or 0
    total_revenue = float(stat.total_revenue) if stat.total_revenue else 0.0
    budget = float(stat.budget) if stat.budget else 0.0
    roi = (total_revenue / budget * 100) if budget > 0 else 0.0

    return {
        "campaign_id": stat.id,
        "campaign_name": stat.name,
        "budget": budget,
        "total_clients": total_clients,
        "active_clients": active_clients,
        "potential_clients": total_clients - active_clients,
        "total_revenue": total_revenue,
        "roi_percentage": round(roi, 2)
    }