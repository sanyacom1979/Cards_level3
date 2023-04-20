
#from typing import Union

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

from dependencies import card_service_dependency

from services.card_service import CardService


from db.base import async_session


router = APIRouter(
    prefix="/cards_api",
    tags=["cards"],
    responses={404: {"description": "Not found"}},
)



class CardCountResponse(BaseModel):
    value: str
    suit: str
    count: int

    class Config:
        orm_mode = True


class BodyToAddCard(BaseModel):
    value: str
    suit: str
    count: int



@router.get("/cards", response_model=CardCountResponse)
async def get_card_count(card_value: str,
    card_suit: str, 
    card_service: CardService=Depends(card_service_dependency),
) -> CardCountResponse:
    card_value = card_value.upper()
    card_suit = card_suit.upper()
    async with async_session() as session:
        async with session.begin():
            res = await card_service.get_card(session, card_value, card_suit)
            if res is None:
                raise HTTPException(status_code=404, detail=f"Card not found")
            return res


@router.get("/_service_route/cards", response_model=CardCountResponse)
async def get_card(card_value: str,
    card_suit: str, 
    card_service: CardService=Depends(card_service_dependency),
) -> CardCountResponse:
    card_value = card_value.upper()
    card_suit = card_suit.upper()
    async with async_session() as session:
        async with session.begin():
            res = await card_service.get_card(session, card_value, card_suit)
            if res is None:
                raise HTTPException(status_code=404, detail=f"Card not found")
            return res


@router.post("/_service_route/cards")
async def add_card(card_item: BodyToAddCard, 
    card_service: CardService=Depends(card_service_dependency),
) -> None:
    async with async_session() as session:
        async with session.begin():
            await card_service.add_card(
                session,
                {
                    "value": card_item.value.upper(),
                    "suit": card_item.suit.upper(),
                    "count": card_item.count,
                }
            )


@router.put("/_service_route/cards")
async def update_card_count(card_value: str,
    card_suit: str,
    card_count: int, 
    card_service: CardService=Depends(card_service_dependency),
) -> None:
    card_value = card_value.upper()
    card_suit = card_suit.upper()
    async with async_session() as session:
        async with session.begin():
            await card_service.update_card_count(session, card_value, card_suit, card_count)