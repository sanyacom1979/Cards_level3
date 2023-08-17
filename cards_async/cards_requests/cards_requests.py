"""
Слой работы с внешней API и записи инфы
из внешней API в БД 
"""

from aiohttp import ClientSession
from cards_async.cards_requests.session import SessionRequests


class ExtAPIRequest:

	def __init__(self, ext_api_base_url: str, my_api_url: str, request_session: SessionRequests) -> None:
		self.ext_api_base_url = ext_api_base_url
		self.my_api_url = my_api_url
		self.request_session = request_session
		self.deck_cache = {}


	async def __call__(self) -> dict:
		if not self.deck_cache:			
			url = f"{self.ext_api_base_url}new/shuffle/?deck_count=1"
			res = await self.request_session.get_url(url)	
			deck_id = res["json"]["deck_id"]
			self.deck_cache["deck_id"] = deck_id
		else:
			url = f"{self.ext_api_base_url}{self.deck_cache['deck_id']}/shuffle/"
			res = await self.request_session.get_url(url)
			deck_id = res["json"]["deck_id"]		
		url = f"{self.ext_api_base_url}{self.deck_cache['deck_id']}/draw/?count=1"
		res = await self.request_session.get_url(url)	
		card = res["json"]["cards"][0]
		url = self.my_api_url
		res = await self.request_session.get_url_params(url, {"card_value": card["value"], "card_suit": card["suit"]})
		card_from_bd = res["json"]
		if res["status"] == 404:
			await self.request_session.post_url(url, {"value": card["value"], "suit": card["suit"], "count": 1})		
		else:
			await self.request_session.put_url(
				url, {
					"card_value": card_from_bd["value"],
					"card_suit": card_from_bd["suit"],
					"card_count": card_from_bd["count"] + 1 
				}
			)				
		return {"value": card["value"], "suit": card["suit"]}