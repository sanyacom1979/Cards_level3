"""
Сервисный слой работы с БД
"""

from typing import Union
from cards_async.db.db_card import DbCards
from cards_async.db.models import Card


class CardService():

	def __init__(self, db: DbCards) -> None:
		self.db_ = db


	async def get_card(self, card_value: str, card_suit: str) -> Union[Card, None]:
		return await self.db_.get(f"(value == {card_value}) & (suit == {card_suit})")


	async def add_card(self, card_row: dict) -> Card:
		return await self.db_.add(card_row)


	async def update_card_count(self, card_value: str, card_suit: str, card_count: int) -> Union[Card, None]:
		return await self.db_.update(f"(value == {card_value}) & (suit == {card_suit})", {"count": card_count})