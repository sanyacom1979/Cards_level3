"""
Cards_level3 небольшой проект по работе с внешней API и базой данных PostgeSQL
Запускаемый модуль: main.py.


Работает с API https://deckofcardsapi.com/

Использует во внешнем API (https://deckofcardsapi.com/) 3 возможности:

- Регистрация колоды с записью уникального номера колоды (deck_id) в КЭШ 
  (пока для КЭШа используется словарь, в плане переход на Redis)
- Вытягивание карты из колоды с записью информации в БД (если карты нет в БД, 
добавляется запись в БД и счетчик устанавливается в значение 1, 
если есть в БД - счетчик увеличивается на 1)
- Возвращение вытянутой карты в колоду и перемешивание колоды.

Для хранения информации используется PostgreSQL
"""

import uvicorn
from fastapi import FastAPI

from cards_async.routes import ext_enpoints, cards_enpoints

app = FastAPI()
app.include_router(ext_enpoints.router)
app.include_router(cards_enpoints.router)


@app.get("/")
async def read_root() -> dict:
    return {"Hello": "World"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
