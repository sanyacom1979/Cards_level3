from sqlalchemy.future import select
from sqlalchemy import update as sqlalchemy_update
from sqlalchemy.ext.asyncio import AsyncSession
from db.base_db import DbBase
from db.models import Card



class DbCards(DbBase):
    
    data_model = Card

    async def get(self, session: AsyncSession, card_value: str, card_suit: str):
        q = select(self.data_model).where((self.data_model.value == card_value) & (self.data_model.suit == card_suit))
        res = await session.execute(q)
        try:
            return res.first()[0]
        except:
            return None


    async def update(self, session: AsyncSession, card_value: str, card_suit: str, upd_data: dict):
        q = (
            sqlalchemy_update(self.data_model)
            .where((self.data_model.value == card_value) & (self.data_model.suit == card_suit))
            .values(upd_data)
            .execution_options(synchronize_session="fetch")
        )
        await session.execute(q)
        await session.commit()


