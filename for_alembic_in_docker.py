"""
Для создания таблиц в докер-контейнере
"""


import alembic
from alembic.config import Config

url = f"postgresql+asyncpg://admin:admin@db:5432/cards"
config = Config("alembic.ini")
config.set_section_option("alembic", "sqlalchemy.url", url)
alembic.command.upgrade(config, "head")