from sqlalchemy import Column, Integer, String
from .base import Base


class Card(Base):
    __tablename__ = "cards"

    id = Column(Integer, primary_key=True, autoincrement=True)
    value = Column(String, nullable=False)
    suit = Column(String, nullable=False)
    count = Column(Integer, nullable=False)
