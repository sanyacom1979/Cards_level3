"""
Тесты сервисного слоя работы с внешней API
"""

import pytest


@pytest.mark.asyncio
async def test_api_service(mock_200, test_ext_api_service) -> None:
	res = await test_ext_api_service()
	assert res == {"value": "4", "suit": "CLUBS"}