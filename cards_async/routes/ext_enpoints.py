"""
Ручки для работы с внешней API
"""

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from cards_async.dependencies import ext_api_service_dependency

from cards_async.services.ext_service import ExtAPIService



router = APIRouter(
    prefix="/ext_api",
    tags=["external_api"],
    responses={404: {"description": "Not found"}},
)


class CardResponse(BaseModel):
    value: str
    suit: str
    

@router.get("/draw_cards", response_model=CardResponse)
async def draw_cards(ext_api_service: ExtAPIService = Depends(ext_api_service_dependency)) -> CardResponse:           
    return await ext_api_service()
