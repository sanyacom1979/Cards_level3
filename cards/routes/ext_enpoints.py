from datetime import date
#from typing import Union

from fastapi import APIRouter#, HTTPException
from pydantic import BaseModel

from cards_requests.cards_requests import cards_requests



router = APIRouter(
    prefix="/ext_api",
    tags=["external_api"],
    responses={404: {"description": "Not found"}},
)


class CardResponse(BaseModel):
    value: str
    suit: str
    

@router.get("/draw_cards", response_model=CardResponse)
async def draw_cards() -> CardResponse:           
    return await cards_requests()
