from decimal import Decimal

import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock
from sqlalchemy import select
from fastapi import Depends
from pydantic import BaseModel
from crud.ad_campaigns import (
    get_ad_campaigns,
    get_ad_campaign_by_id,
    get_ad_campaign_by_name,
    create_ad_campaign,
    update_ad_campaign,
    delete_ad_campaign,
)
from models.ad_campaigns import AdCampaign
from schemas.ad_campaigns import AdCampaignCreate, AdCampaignUpdate

# Фиктивные данные для тестов
class MockAdCampaign:
    def __init__(self, id=1, name="Campaign", service_id=1, channel="Test Campaign", budget=Decimal("100")):
        self.id = id
        self.name = name
        self.service_id = service_id
        self.channel = channel
        self.budget = budget

# Настройка pytest-asyncio
pytestmark = pytest.mark.asyncio

# Тест для get_ad_campaigns
async def test_get_ad_campaigns():
    # Создаем мок для AsyncSession
    mock_db = AsyncMock()
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = [
        MockAdCampaign(id=1, name="Campaign 1", service_id=1, channel="Test Campaign", budget=Decimal("100")),
        MockAdCampaign(id=2, name="Campaign 2", service_id=2, channel="Test Campaign 2", budget=Decimal("200")),
    ]
    mock_db.execute.return_value = mock_result

    # Вызываем функцию
    result = await get_ad_campaigns(skip=0, limit=2, db=mock_db)

    # Проверяем вызовы и результат
    mock_db.execute.assert_called_once()
    assert len(result) == 2
    assert result[0].id == 1
    assert result[0].name == "Campaign 1"
    assert result[0].service_id == 1
    assert result[0].channel == "Test Campaign"
    assert result[0].budget == Decimal("100")
    assert result[1].id == 2
    assert result[1].name == "Campaign 2"
    assert result[1].service_id == 2
    assert result[1].channel == "Test Campaign 2"
    assert result[1].budget == Decimal("200")

# Тест для get_ad_campaign_by_id
async def test_get_ad_campaign_by_id():
    # Создаем мок для AsyncSession
    mock_db = AsyncMock()
    mock_result = MagicMock()
    mock_result.scalars.return_value.one_or_none.return_value = MockAdCampaign(id=1, name="Test Campaign", service_id=1, channel="Test Campaign", budget=Decimal("100"))
    mock_db.execute.return_value = mock_result

    # Вызываем функцию
    result = await get_ad_campaign_by_id(ad_campaign_id=1, db=mock_db)

    # Проверяем вызовы и результат
    mock_db.execute.assert_called_once()
    assert result.id == 1
    assert result.name == "Campaign 1"
    assert result.service_id == 1
    assert result.channel == "Test Campaign"
    assert result.budget == Decimal("100")

# Тест для get_ad_campaign_by_id (случай, когда кампания не найдена)
async def test_get_ad_campaign_by_id_not_found():
    # Создаем мок для AsyncSession
    mock_db = AsyncMock()
    mock_result = MagicMock()
    mock_result.scalars.return_value.one_or_none.return_value = None
    mock_db.execute.return_value = mock_result

    # Вызываем функцию
    result = await get_ad_campaign_by_id(ad_campaign_id=999, db=mock_db)

    # Проверяем вызовы и результат
    mock_db.execute.assert_called_once()
    assert result is None

# Тест для get_ad_campaign_by_name
async def test_get_ad_campaign_by_name():
    # Создаем мок для AsyncSession
    mock_db = AsyncMock()
    mock_result = MagicMock()
    mock_result.scalars.return_value.one_or_none.return_value = MockAdCampaign(id=1, name="Campaign 1", service_id=1, channel="Test Campaign", budget=Decimal("100"))
    mock_db.execute.return_value = mock_result

    # Вызываем функцию
    result = await get_ad_campaign_by_name(name="Test Campaign", db=mock_db)

    # Проверяем вызовы и результат
    mock_db.execute.assert_called_once()
    assert result.id == 1
    assert result.name == "Test Campaign"

# Тест для create_ad_campaign
async def test_create_ad_campaign():
    # Создаем мок для AsyncSession
    mock_db = AsyncMock()
    ad_campaign_data = AdCampaignCreate(name="New Campaign")
    mock_ad_campaign = MockAdCampaign(id=1, name="New Campaign", service_id=1, channel="Test Campaign", budget=Decimal("100"))
    mock_db.add = MagicMock()
    mock_db.commit = AsyncMock()
    mock_db.refresh = AsyncMock()

    # Вызываем функцию
    result = await create_ad_campaign(ad_campaign=ad_campaign_data, db=mock_db)

    # Проверяем вызовы и результат
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()
    assert result.name == "New Campaign"

# Тест для update_ad_campaign
async def test_update_ad_campaign():
    # Создаем мок для AsyncSession
    mock_db = AsyncMock()
    ad_campaign_data = AdCampaignUpdate(id=1, name="Updated Campaign")
    mock_ad_campaign = MockAdCampaign(id=1, name="Original Campaign")
    mock_db.commit = AsyncMock()
    mock_db.refresh = AsyncMock()

    # Вызываем функцию
    result = await update_ad_campaign(ad_campaign=ad_campaign_data, db=mock_db)

    # Проверяем вызовы и результат
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()
    assert result.name == "Updated Campaign"

# Тест для delete_ad_campaign
async def test_delete_ad_campaign():
    # Создаем мок для AsyncSession
    mock_db = AsyncMock()
    mock_db.delete = AsyncMock()
    mock_db.commit = AsyncMock()
    mock_db.refresh = AsyncMock()

    # Вызываем функцию
    result = await delete_ad_campaign(ad_campaign_id=1, db=mock_db)

    # Проверяем вызовы и результат
    mock_db.delete.assert_called_once()
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()
    assert result is None