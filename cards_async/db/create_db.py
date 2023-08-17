"""
Модуль создания таблиц БД (в проекте не используется)
"""

from cards_async.db.base import engine
from cards_async.db.models import Base, Card

async with engine.begin() as conn:
	await conn.run_sync(Base.metadata.drop_all)
	await conn.run_sync(Base.metadata.create_all(tables=[Card.__table__]))