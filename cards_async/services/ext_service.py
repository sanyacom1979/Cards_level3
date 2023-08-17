"""
Сервисный слой работы с внешней API
"""

from cards_async.cards_requests.cards_requests import ExtAPIRequest

class ExtAPIService:

	def __init__(self, ext_api_request: ExtAPIRequest) -> None:
		self._ext_api_request = ext_api_request


	async def __call__(self) -> dict:
		return await self._ext_api_request()