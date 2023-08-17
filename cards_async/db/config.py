"""
Конфиг для работы с БД.
Использует переменные окружения.
"""

from pydantic import BaseSettings
from environs import Env

env = Env()
env.read_env()


class DatabaseConfig(BaseSettings):
    login: str = env.str("DB_LOGIN")
    password: str = env.str("DB_PASSWORD")
    host: str = env.str("DB_HOST")
    port: str = env.str("DB_PORT")
    database: str = env.str("DB_DATABASE")
