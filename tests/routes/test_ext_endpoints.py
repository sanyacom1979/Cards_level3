"""
Тесты ручек работы с внешней API
"""

import pytest


@pytest.mark.asyncio
async def test_draw_cards(async_client) -> None:
	response = await async_client.get("http://testserver/ext_api/draw_cards")
	assert response.status_code == 200
	data = response.json()
	assert data == {"value": "4", "suit": "CLUBS"}