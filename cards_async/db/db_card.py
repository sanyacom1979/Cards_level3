"""
Базовый слой работы с БД cards
"""

from cards_async.db.base_db import DbBase
from cards_async.db.models import Card


class DbCards(DbBase):  
    data_model = Card
