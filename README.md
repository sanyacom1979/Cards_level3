# Cards_level3

## О проекте

**Cards_level3** небольшой проект по работе с внешней API и базой данных PostgeSQL
Запускаемый модуль: **main.py**.


Работает с API https://deckofcardsapi.com/

Использует во внешнем API (https://deckofcardsapi.com/) 3 возможности:

- Регистрация колоды с записью уникального номера колоды (deck_id) в КЭШ 
  (пока для КЭШа используется словарь, в плане переход на Redis)
- Вытягивание карты из колоды с записью информации в БД (если карты нет в БД, добавляется запись в БД и счетчик
  устанавливается в значение 1, если есть в БД - счетчик увеличивается на 1)
- Возвращение вытянутой карты в колоду и перемешивание колоды.

Для хранения информации используется **PostgreSQL**

## Начать работу

Для установки **Cards_level3** необходимо выполнить следующую команду

```console
$ git clone https://github.com/sanyacom1979/Cards_level3.git
```

Для корректной работы Вам понадобится установка следующих библиотек: **aiohttp, alembic, anyio, asyncpg, fastapi, psycopg2, pydantic, SQLAlchemy, typing-extensions, uvicorn**.

Установить библиотеки можно из консоли

```console
$ pip install fastapi
```
Также понабится установка **PostreSQL**. Если хотите наглядно выдеть результат работы в **PostreSQL**, то нужно установить програмный продукт для работы с БД (например: **DBeaver**).

## Работа программы

Реализовано 5 роутов FastAPI:

1. **http://127.0.0.1:8080/ext_api/draw_cards/**  -  (get) роут для работы с внешней API (https://deckofcardsapi.com/) 
2. **http://127.0.0.1:8080/cards_api/cards/**     - (get) роут для получения информации о количесте выпаданий запрошенной карты из БД 
3. **http://127.0.0.1:8080/cards_api/_service_route/cards** - (get, post, put) сервисные роуты для связи внешней API c БД 

Роут 1. получает получает карту с внешней API и с помощью роутов 3. проверяет карту в БД и, в зависимости от результата, добавляет и карту в БД или обновляет количество выпаданий карты. 

## Технологии, использованные в проекте

### FastAPI

```python
@router.get("/draw_cards", response_model=CardResponse)
async def draw_cards() -> CardResponse:           
    return await cards_requests()
```

### Pydantic

```python
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
```

### Typing

```python
@router.get("/_service_route/cards", response_model=CardCountResponse)
async def get_card(card_value: str,
    card_suit: str, 
    card_service: CardService=Depends(card_service_dependency),
) -> CardCountResponse:
```

### Dependency Injection

```python
card_service: CardService=Depends(card_service_dependency)
```
```python

def db_dependency() -> DbCards: 
	return DbCards()


def card_service_dependency(
	db: DbCards = Depends(db_dependency)
) -> CardService:
	
	return CardService(db)

```

### SQLAlchemy

```python
db_url = f"postgresql+asyncpg://{config.login}:{config.password}@{config.host}:{config.port}/{config.database}"
engine = create_async_engine(db_url)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


class Base(DeclarativeBase):
    ...
```

```python
class Card(Base):
    __tablename__ = "cards"

    id = Column(Integer, primary_key=True, autoincrement=True)
    value = Column(String, nullable=False)
    suit = Column(String, nullable=False)
    count = Column(Integer, nullable=False)

```

```python
class DbBase():

    data_model = None

    
    async def add(self, session: AsyncSession, data: dict):
        to_add = self.data_model(**data)
        session.add(to_add)
        await session.commit()



    async def get(self, session: AsyncSession, filt: str):
       ...

    
    async def update(self, session: AsyncSession, filt: str, upd_data: dict):
        ...
```

```python
class DbCards(DbBase):
    
    data_model = Card

    async def get(self, session: AsyncSession, card_value: str, card_suit: str):
        q = select(self.data_model).where((self.data_model.value == card_value) & (self.data_model.suit == card_suit))
        res = await session.execute(q)
        try:
            return res.first()[0]
        except:
            return None


    async def update(self, session: AsyncSession, card_value: str, card_suit: str, upd_data: dict):
        q = (
            sqlalchemy_update(self.data_model)
            .where((self.data_model.value == card_value) & (self.data_model.suit == card_suit))
            .values(upd_data)
            .execution_options(synchronize_session="fetch")
        )
        await session.execute(q)
        await session.commit()
```

### AioHTTP

```python
async with ClientSession() as session:
		url = f"https://deckofcardsapi.com/api/deck/{deck_cache['deck_id']}/draw/?count=1"
		async with session.get(url=url) as resp:
			res = await resp.json()
			card = res["cards"][0]
```

## Авторы

Александр Городецкий - г. Псков - sanyacom@mail.ru или alexandr_gorodetskiy@mail.ru

## Лицензия

Данный проект использует лицензию Apache 2.0.
Ознакомиться с лицензией можно [здесь](https://github.com/sanyacom1979/Cards_level3/blob/main/LICENSE)