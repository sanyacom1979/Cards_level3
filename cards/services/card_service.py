from db.db_card import DbCards

from sqlalchemy.ext.asyncio import AsyncSession

class CardService():

	def __init__(self, db: DbCards):
		self.db_ = db


	async def get_card(self, session: AsyncSession, card_value: str, card_suit: str):
		return await self.db_.get(session, card_value, card_suit)


	async def add_card(self, session: AsyncSession, card_row: dict):
		await self.db_.add(session, card_row)


	async def update_card_count(self, session: AsyncSession, card_value: str, card_suit: str, card_count: int):
		await self.db_.update(session, card_value, card_suit, {"count": card_count})