"""
Тесты БД
"""

import pytest
from cards_async.db.models import Card
from sqlalchemy.sql.elements import BooleanClauseList


value = "4"
suit = "CLUBS"


@pytest.mark.asyncio
async def test_add(test_db) -> None:	
	chk_data = {"value": value, "suit": suit, "count": 1}
	res = await test_db.add(chk_data)
	assert await res.to_dict() == chk_data
	await test_db.delete(f"(value == {value}) & (suit == {suit})")



@pytest.mark.asyncio
@pytest.mark.parametrize(
    "t_value, t_suit, chk_data",[
        (
            "4",
            "CLUBS", 
            {"value": "4", "suit": "CLUBS", "count": 1}
        ),
        (
            "5",
            "CLUBS", 
            None
        )
    ]
)
async def test_get(test_db, t_value, t_suit, chk_data) -> None:
	add_data = {"value": value, "suit": suit, "count": 1}
	await test_db.add(add_data)
	res = await test_db.get(f"(value == {t_value}) & (suit == {t_suit})")
	if isinstance(res, Card):
		assert await res.to_dict() == chk_data
	else:
		assert res == chk_data
	await test_db.delete(f"(value == {value}) & (suit == {suit})")



@pytest.mark.asyncio
@pytest.mark.parametrize(
    "t_value, t_suit, chk_data",[
        (
            "4",
            "CLUBS", 
            {"value": "4", "suit": "CLUBS", "count": 2}
        ),
        (
            "5",
            "CLUBS", 
            None
        )
    ]
)
async def test_update(test_db, t_value, t_suit, chk_data) -> None:
	add_data = {"value": value, "suit": suit, "count": 1}
	await test_db.add(add_data)
	res = await test_db.update(f"(value == {t_value}) & (suit == {t_suit})", {"count": 2})
	if isinstance(res, Card):
		assert await res.to_dict() == chk_data
	else:
		assert res == chk_data
	await test_db.delete(f"(value == {value}) & (suit == {suit})")



@pytest.mark.asyncio
async def test_delete(test_db) -> None:
	add_data = {"value": value, "suit": suit, "count": 1}
	await test_db.add(add_data)
	await test_db.delete(f"(value == {value}) & (suit == {suit})")
	res = await test_db.get(f"(value == {value}) & (suit == {suit})")
	assert res is None



@pytest.mark.asyncio
async def test_conv_where(test_db) -> None:
	res = await test_db._conv_where(f"(value == {value}) & (suit == {suit})")
	assert isinstance(res, BooleanClauseList) == True

