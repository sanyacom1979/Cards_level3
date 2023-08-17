"""
Кординационный тестовый модуль.
Содержит фикстуры для тестирования проекта.
Непосредственно тестов не содержит.
Разделен на секции для тестирования слоев ручек, БД и внешней API
"""

import pytest
import json
from contextlib import asynccontextmanager
import alembic
from alembic.config import Config
from httpx import AsyncClient
from typing import Union
from aioresponses import aioresponses
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from testcontainers.postgres import PostgresContainer
from cards_async.main import app
from cards_async.db.base import Database
from cards_async.db.base_db import DbBase
from cards_async.db.db_card import DbCards
from cards_async.services.card_service import CardService
from cards_async.cards_requests.cards_requests import ExtAPIRequest
from cards_async.services.ext_service import ExtAPIService
from cards_async.cards_requests.config import RequestConfig
from cards_async.cards_requests.session import SessionControl, SessionRequests
from cards_async.dependencies import db_dependency, ext_api_request_dependency


class TestDbCardsOK(DbBase):

    def __init__(self):
        ...


    async def get(self, card_cond: None = None) -> dict:
        return {"value": "4", "suit": "CLUBS", "count": 2}


    async def add(self, data: None = None) -> dict:
        return {"value": "4", "suit": "CLUBS", "count": 2}


    async def update(self, card_cond: None = None, upd_data: None = None) -> dict:
        return {"value": "4", "suit": "CLUBS", "count": 2}



class TestDbCardsErr(DbBase):

    def __init__(self):
        ...

    async def get(self, card_cond: None = None) -> None:
        return None


    async def update(self, card_cond: None = None, upd_data: None = None) -> None:
        return None



class TestExtApiRequest(ExtAPIRequest):

    def __init__(self):
        ...


    async def __call__(self) -> dict:
        return {"value": "4", "suit": "CLUBS"}



def override_db_dependency(for_testing: str) -> Union[TestDbCardsOK, TestDbCardsErr]:
    if for_testing == "Err":
        return TestDbCardsErr()
    return TestDbCardsOK()



def override_ext_api_request_dependency() -> TestExtApiRequest:
    return TestExtApiRequest()


app.dependency_overrides[db_dependency] = override_db_dependency
app.dependency_overrides[ext_api_request_dependency] = override_ext_api_request_dependency


@pytest.fixture
def async_client() -> AsyncClient:
    yield AsyncClient(app=app)


#-------------------------------------------------------------------------------------------------

@pytest.fixture()
def test_db_session() -> Database:
    with PostgresContainer("postgres:15.2") as postgres:
        postgres.driver = "asyncpg"
        url = postgres.get_connection_url()  
        config = Config("alembic.ini")
        config.set_section_option("alembic", "sqlalchemy.url", url)
        alembic.command.upgrade(config, "head")
        yield Database(url)
        alembic.command.downgrade(config, "base")



@pytest.fixture
def test_db(test_db_session) -> DbCards:
    return DbCards(test_db_session.get_session)


@pytest.fixture
def test_service(test_db) -> CardService:
    return CardService(test_db)


#-------------------------------------------------------------------------------------------------------


@pytest.fixture
def test_request_config() -> RequestConfig:
    return RequestConfig()


@pytest.fixture
def test_session_control() -> SessionControl:
    return SessionControl()


@pytest.fixture
def test_session_requests(test_session_control) -> SessionRequests:
    return SessionRequests(test_session_control.get_session)


@pytest.fixture
def test_ext_api_request(test_request_config, test_session_requests) -> ExtAPIRequest:
    return ExtAPIRequest(test_request_config.ext_api_base_url, test_request_config.my_api_url, test_session_requests)


@pytest.fixture
def test_ext_api_service(test_ext_api_request) -> ExtAPIService:
    return ExtAPIService(test_ext_api_request)


@pytest.fixture
def mocked():
    with aioresponses() as m:
        yield m



@pytest.fixture
def mock_200(mocked, test_ext_api_request) -> None:
    deck_id = "111111111111"
    value = "4"
    suit = "CLUBS"
    mocked.get(
        f"{test_ext_api_request.ext_api_base_url}new/shuffle/?deck_count=1",
        status=200, 
        body=json.dumps({"success": True, "deck_id": deck_id, "remaining": 52, "shuffled": True})
    )
    mocked.get(
        f"{test_ext_api_request.ext_api_base_url}{deck_id}/shuffle/",
        status=200, 
        body=json.dumps({"success": True, "deck_id": deck_id, "remaining": 52, "shuffled": True})
    )
    mocked.get(
        f"{test_ext_api_request.ext_api_base_url}{deck_id}/draw/?count=1", 
        status=200,
        body=json.dumps(
            {          
                "success": True, 
                "deck_id": deck_id, 
                "cards": [
                    {
                        "code": "5H", 
                        "image": "https://deckofcardsapi.com/static/img/5H.png", 
                        "images": {
                            "svg": "https://deckofcardsapi.com/static/img/5H.svg", 
                            "png": "https://deckofcardsapi.com/static/img/5H.png"
                        }, 
                        "value": value, 
                        "suit": suit
                    }
                ], 
                "remaining": 51         
            }
        )
    )
    mocked.get(
        f"{test_ext_api_request.my_api_url}?card_suit={suit}&card_value={value}",
        status=200,
        body=json.dumps({"value": value, "suit": suit, "count": 1})
    )
    mocked.post(
        test_ext_api_request.my_api_url,
        status=200,
        body=json.dumps({"value": value, "suit": suit, "count": 1})
    )
    mocked.put(
        f"{test_ext_api_request.my_api_url}?card_count=2&card_suit={suit}&card_value={value}",
        status=200,
        body=json.dumps({"value": value, "suit": suit, "count": 2})
    )