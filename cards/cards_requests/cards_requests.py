from aiohttp import ClientSession
from fastapi import HTTPException

deck_cache = {}


async def cards_requests() -> dict:
	if not deck_cache:
		async with ClientSession() as session:
			url = "https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1"
			async with session.get(url=url) as resp:
				res = await resp.json()
				deck_id = res["deck_id"]
		deck_cache["deck_id"] = deck_id
	else:
		async with ClientSession() as session:
			url = f"https://deckofcardsapi.com/api/deck/{deck_cache['deck_id']}/shuffle/"
			async with session.get(url=url) as resp:
				res = await resp.json()
				deck_id = res["deck_id"]
	async with ClientSession() as session:
		url = f"https://deckofcardsapi.com/api/deck/{deck_cache['deck_id']}/draw/?count=1"
		async with session.get(url=url) as resp:
			res = await resp.json()
			card = res["cards"][0]
	async with ClientSession() as session:
		url = "http://127.0.0.1:8080/cards_api/_service_route/cards"
		async with session.get(url=url, params={"card_value": card["value"], "card_suit": card["suit"]}) as resp:
			try:
				card_from_bd = await resp.json()
			except:	
				async with ClientSession() as session:
					async with session.post(url=url, json={"value": card["value"], "suit": card["suit"], "count": 1}) as resp:
						await resp.json()
			else:
				async with ClientSession() as session:
					async with session.put(
						url=url, params={
							"card_value": card_from_bd["value"], 
							"card_suit": card_from_bd["suit"], 
							"card_count": card_from_bd["count"] + 1
						}
					) as resp:
						await resp.json()
	return {"value": card["value"], "suit": card["suit"]}

