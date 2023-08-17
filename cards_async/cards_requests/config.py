"""
Конфиг. Содержит адреса выхода на внешнее API и на FastAPI
"""

from pydantic import BaseSettings


class RequestConfig(BaseSettings):

	ext_api_base_url: str = "https://deckofcardsapi.com/api/deck/"
	my_api_url: str = "http://127.0.0.1:8080/cards_api/_service_route/cards"
