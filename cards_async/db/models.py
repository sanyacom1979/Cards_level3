"""
Модуль моделей для БД
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    ...


class Card(Base):
    __tablename__ = "cards"

    id = Column(Integer, primary_key=True, autoincrement=True)
    value = Column(String, nullable=False)
    suit = Column(String, nullable=False)
    count = Column(Integer, nullable=False)


    async def to_dict(self):
        return {"value": self.value, "suit": self.suit, "count": self.count}