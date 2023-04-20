from fastapi import Depends

from db.db_card import DbCards
from services.card_service import CardService


def db_dependency() -> DbCards: 
	return DbCards()


def card_service_dependency(
	db: DbCards = Depends(db_dependency)
) -> CardService:
	
	return CardService(db)

