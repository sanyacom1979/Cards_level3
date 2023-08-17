"""
Модуль зависимостей. 
Осуществляет взаимодействие между слоями проекта
"""

from fastapi import Depends
from cards_async.db.base import Database
from cards_async.db.config import DatabaseConfig
from cards_async.db.db_card import DbCards
from cards_async.services.card_service import CardService
from cards_async.cards_requests.config import RequestConfig
from cards_async.cards_requests.cards_requests import ExtAPIRequest
from cards_async.services.ext_service import ExtAPIService
from cards_async.cards_requests.session import SessionRequests
from cards_async.cards_requests.session import SessionControl


def db_config_dependency() -> DatabaseConfig:
	return DatabaseConfig()


def db_base_dependency(
	db_config: DatabaseConfig = Depends(db_config_dependency)
	) -> Database:
	return Database(f"postgresql+asyncpg://{db_config.login}:{db_config.password}@{db_config.host}:{db_config.port}/{db_config.database}")


def db_dependency(
	db_base: Database = Depends(db_base_dependency)
	) -> DbCards: 
	return DbCards(db_base.get_session)


def card_service_dependency(
	db: DbCards = Depends(db_dependency)
) -> CardService:
	
	return CardService(db)

#-----------------------------------------------------

def request_config_dependency() -> RequestConfig:
	return RequestConfig()


def session_control_dependency() -> SessionControl:
	return SessionControl()


def session_request_dependency(
	session_control: SessionControl = Depends(session_control_dependency)
) -> SessionRequests:
	return SessionRequests(session_control.get_session)


def ext_api_request_dependency(
	request_config: RequestConfig = Depends(request_config_dependency),
	request_session: SessionRequests = Depends(session_request_dependency)
) -> ExtAPIRequest:
	return ExtAPIRequest(request_config.ext_api_base_url, request_config.my_api_url, request_session)


def ext_api_service_dependency(
	ext_api_request: ExtAPIRequest = Depends(ext_api_request_dependency)
) -> ExtAPIService:
	return ExtAPIService(ext_api_request)

