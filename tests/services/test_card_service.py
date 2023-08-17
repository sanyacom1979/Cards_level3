"""
Тесты сервисного слоя работы с БД
"""

import pytest

value = "4"
suit = "CLUBS"


@pytest.mark.asyncio
async def test_add_card(test_service, test_db) -> None:	
	chk_data = {"value": value, "suit": suit, "count": 1}
	res = await test_service.add_card(chk_data)
	assert await res.to_dict() == chk_data
	await test_db.delete(f"(value == {value}) & (suit == {suit})")


@pytest.mark.asyncio
async def test_get_card(test_service, test_db) -> None:
	chk_data = {"value": value, "suit": suit, "count": 1}
	await test_db.add(chk_data)
	res = await test_service.get_card(card_value="4", card_suit="CLUBS")
	assert await res.to_dict() == chk_data
	await test_db.delete(f"(value == {value}) & (suit == {suit})")



@pytest.mark.asyncio
async def test_update_card_count(test_service, test_db) -> None:
	add_data = {"value": value, "suit": suit, "count": 1}
	chk_data = {"value": value, "suit": suit, "count": 2}
	await test_db.add(add_data)
	res = await test_service.update_card_count(card_value="4", card_suit="CLUBS", card_count=2)
	assert await res.to_dict() == chk_data
	await test_db.delete(f"(value == {value}) & (suit == {suit})")

