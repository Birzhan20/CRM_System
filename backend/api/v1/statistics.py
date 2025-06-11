from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict
from core.database import get_db
from crud.statistics import get_campaign_stats, get_campaign_stats_by_id
from crud.users import require_role
from models.users import User
from schemas.users import UserRole

router = APIRouter(prefix="/statistics", tags=["Analytics"])


@router.get("/campaigns", response_model=List[Dict], status_code=200)
async def get_all_campaign_stats(db: AsyncSession = Depends(get_db),
                                 current_user: User = Depends(require_role(
                                     [UserRole.ADMIN, UserRole.OPERATOR, UserRole.MANAGER, UserRole.MARKETER]))):
    """
    Получение статистики по всем рекламным кампаниям.
    """
    stats = await get_campaign_stats(db)
    return stats


@router.get("/campaigns/{campaign_id}", response_model=Dict, status_code=200)
async def get_campaign_stats_detail(campaign_id: int, db: AsyncSession = Depends(get_db),
                                    current_user: User = Depends(require_role(
                                        [UserRole.ADMIN, UserRole.OPERATOR, UserRole.MANAGER, UserRole.MARKETER]))):
    """
    Получение статистики по конкретной рекламной кампании.
    """
    stat = await get_campaign_stats_by_id(db, campaign_id)
    if not stat:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return stat

# подсчёт и отображение статистики по рекламным кампаниям:
# сколько привлечено потенциальных клиентов, сколько из них перешло в активных.
#
# Подсчёт статистики об успешности рекламных кампаний
# Статистику считают по нескольким критериям:
# число клиентов, привлечённых рекламной кампанией;
# число клиентов, перешедших из потенциальных в активных;
# соотношение дохода от контрактов и расходов на рекламу.
#
# CRM-cистема должна считать статистику успешности рекламных кампаний и учитывать несколько факторов:
# количество потенциальных клиентов, заинтересовавшихся рекламой;
# количество переходов клиентов из потенциальных в активные;
# объёмы продаж по клиентам.
