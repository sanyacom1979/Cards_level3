"""
Тесты слоя работы с внешней API
"""

import pytest


@pytest.mark.asyncio
async def test_api_request(mock_200, test_ext_api_request) -> None:
	res = await test_ext_api_request()
	assert res == {"value": "4", "suit": "CLUBS"}