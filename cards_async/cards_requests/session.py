"""
Самые низкие слои для работы с aiohttp.
Открытие сессии и базовые http-запросы
"""

from contextlib import asynccontextmanager
from aiohttp import ClientSession

class SessionControl:

	@asynccontextmanager
	async def get_session(self) -> ClientSession:
		session = ClientSession()
		yield session
		await session.close()


class SessionRequests:

	def __init__(self, session: ClientSession) -> None:
		self.session = session


	async def get_url(self, url: str) -> dict:       
		async with self.session() as session: 
			async with session.get(url) as response:
				if response.status == 200: 
					json_result = await response.json()
					return {"status": 200, "json": json_result, "msg": None}
				elif response.status == 404:
					return {"status": 404, "json": None, "msg": "Not found"}
				else:
					return {"status": response.status, "json": None, "msg": await response.text()}
        

	async def get_url_params(self, url: str, params: dict) -> dict:
		async with self.session() as session:
			async with session.get(url, params=params) as response:
				if response.status == 200: 
					json_result = await response.json()
					return {"status": 200, "json": json_result, "msg": None}
				elif response.status == 404:
					return {"status": 404, "json": None, "msg": "Not found"}
				else:
					return {"status": response.status, "json": None, "msg": await response.text()}


	async def post_url(self, url: str, json: dict) -> dict:
		async with self.session() as session:
			async with session.post(url, json=json) as response:      
				if response.status == 200: 
					json_result = await response.json()
					return {"status": 200, "json": json_result, "msg": None}
				else:
					return {"status": response.status, "json": None, "msg": await response.text()}


	async def put_url(self, url: str, params: dict) -> dict:
		async with self.session() as session:        
			async with session.put(url, params=params) as response:
				if response.status == 200: 
					json_result = await response.json()
					return {"status": 200, "json": json_result, "msg": None}
				elif response.status == 404:
					return {"status": 404, "json": None, "msg": "Not found"}
				else:
					return {"status": response.status, "json": None, "msg": await response.text()}
        
