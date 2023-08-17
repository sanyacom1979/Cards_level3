"""
Базовый слой работы с абстрактной БД
"""

from operator import and_, or_, eq, ne, ge, le, gt, lt
from typing import Any
from sqlalchemy.sql.elements import BooleanClauseList
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update as sqlalchemy_update

class DbBase():

    data_model = None

    
    def __init__(self, session: AsyncSession) -> None:
        self.session = session


    async def add(self, data: dict) -> Any:
        async with self.session() as session:
            async with session.begin():
                to_add = self.data_model(**data)
                session.add(to_add)
                await session.commit()
                return to_add


    
    async def get(self, card_cond: str) -> Any:     
        async with self.session() as session:
            async with session.begin():
                q = select(self.data_model).where(await self._conv_where(card_cond))
                res = await session.execute(q)
                try:
                    return res.first()[0]
                except:
                    return None


    async def update(self, card_cond: str, upd_data: dict) -> Any:   
        async with self.session() as session:
            async with session.begin():
                q = (
                    sqlalchemy_update(self.data_model)
                    .where(await self._conv_where(card_cond))
                    .values(upd_data)
                    .execution_options(synchronize_session="fetch")
                    .returning(self.data_model)
                )
                res = await session.execute(q)
                await session.commit()
                try:
                    return res.first()[0]
                except:
                    return None


    async def delete(self, card_cond: str) -> None:
        async with self.session() as session:
            async with session.begin():
                q = select(self.data_model).where(await self._conv_where(card_cond))
                res = await session.execute(q)
                try:
                    to_delete = res.first()[0]
                    await session.delete(to_delete)
                    await session.commit()
                except:
                    ...


    async def _conv_where(self, card_cond: str) -> BooleanClauseList:
        for _ in range(2):
            counter = 0
            for i, c in enumerate(card_cond):
                if c == "(":
                    counter += 1
                elif c == ")":
                    counter -= 1
                else:
                    if counter == 0:
                        if c == "&":
                            return and_(await self._conv_where(card_cond[:i].strip()), await self._conv_where(card_cond[i + 1:].strip()))
                        if c == "|":
                            return or_(await self._conv_where(card_cond[:i].strip()), await self._conv_where(card_cond[i + 1:].strip()))
            if card_cond.startswith("("):
                card_cond = card_cond[1:-1]
            else: 
                break
        c = card_cond.split("==")
        if c[1:]:
            return eq(getattr(self.data_model, c[0].strip()), c[1].strip())
        c = card_cond.split("!=")
        if c[1:]:
            return ne(getattr(self.data_model, c[0].strip()), c[1].strip())
        c = card_cond.split(">=")
        if c[1:]:
            return ge(getattr(self.data_model, c[0].strip()), c[1].strip())
        c = card_cond.split("<=")
        if c[1:]:
            return le(getattr(self.data_model, c[0].strip()), c[1].strip())
        c = card_cond.split(">")
        if c[1:]:
            return gt(getattr(self.data_model, c[0].strip()), c[1].strip())
        c = card_cond.split("<")
        if c[1:]:
            return lt(getattr(self.data_model, c[0].strip()), c[1].strip())
