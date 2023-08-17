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

Для корректной работы Вам понадобится установка следующих библиотек: **aiohttp, alembic, anyio, asyncpg, fastapi, pydantic, SQLAlchemy, typing-extensions, environs, uvicorn**.

Установить библиотеки можно из консоли

```console
$ pip install fastapi
```
Также понабится установка **PostreSQL**. Если хотите наглядно выдеть результат работы в **PostreSQL**, то нужно установить програмный продукт для работы с БД (например: **DBeaver**).

## Работа программы

Реализовано 5 роутов FastAPI:

1. ...localhost.../ext_api/draw_cards/                 -  (get) роут для работы с внешней API (https://deckofcardsapi.com/) 
2. ...localhost.../cards_api/cards/                    - (get) роут для получения информации о количесте выпаданий запрошенной карты из БД 
3. ...localhost.../cards_api/_service_route/cards      - (get, post, put) сервисные роуты для связи внешней API c БД __

Роут 1. получает получает карту с внешней API и с помощью роутов 3. проверяет карту в БД и, в зависимости от результата, добавляет и карту в БД или обновляет количество выпаданий карты. 

## Технологии, использованные в проекте

### FastAPI

```python
@router.get("/draw_cards", response_model=CardResponse)
async def draw_cards(ext_api_service: ExtAPIService = Depends(ext_api_service_dependency)) -> CardResponse:           
    return await ext_api_service()
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

def db_config_dependency() -> DatabaseConfig:
    return DatabaseConfig()


def db_base_dependency(
    db_config: DatabaseConfig = Depends(db_config_dependency)
    ) -> Database:
    return Database(f"postgresql+asyncpg://{db_config.login}:{db_config.password}@{db_config.host}:{db_config.port}/{db_config.database}")


def db_dependency(
    db_base: Database = Depends(db_base_dependency)
    ) -> DbCards: 
    return DbCards(db_base.get_session)


def card_service_dependency(
    db: DbCards = Depends(db_dependency)
) -> CardService:
    
    return CardService(db)

```

### SQLAlchemy

```python
class Database:

    def __init__(self, db_url: str) -> None:
        self.db_url = db_url 
        self._engine = create_async_engine(self.db_url)
        self._async_session = sessionmaker(bind=self._engine, expire_on_commit=False, class_=AsyncSession)


    @asynccontextmanager
    async def get_session(self) -> AsyncSession:
        session = self._async_session()
        yield session
        await session.close()
    ...
```

```python
class Base(DeclarativeBase):
    ...


class Card(Base):
    __tablename__ = "cards"

    id = Column(Integer, primary_key=True, autoincrement=True)
    value = Column(String, nullable=False)
    suit = Column(String, nullable=False)
    count = Column(Integer, nullable=False)


    async def to_dict(self):
        return {"value": self.value, "suit": self.suit, "count": self.count}

```

```python
class DbBase():

    data_model = None

    
    def __init__(self, session: AsyncSession) -> None:
        self.session = session


    async def add(self, data: dict) -> Any:
        async with self.session() as session:
            async with session.begin():
                to_add = self.data_model(**data)
                session.add(to_add)
                await session.commit()
                return to_add


    
    async def get(self, card_cond: str) -> Any:     
        async with self.session() as session:
            async with session.begin():
                q = select(self.data_model).where(await self._conv_where(card_cond))
                res = await session.execute(q)
                try:
                    return res.first()[0]
                except:
                    return None


    async def update(self, card_cond: str, upd_data: dict) -> Any:   
        async with self.session() as session:
            async with session.begin():
                q = (
                    sqlalchemy_update(self.data_model)
                    .where(await self._conv_where(card_cond))
                    .values(upd_data)
                    .execution_options(synchronize_session="fetch")
                    .returning(self.data_model)
                )
                res = await session.execute(q)
                await session.commit()
                try:
                    return res.first()[0]
                except:
                    return None


    async def delete(self, card_cond: str) -> None:
        async with self.session() as session:
            async with session.begin():
                q = select(self.data_model).where(await self._conv_where(card_cond))
                res = await session.execute(q)
                try:
                    to_delete = res.first()[0]
                    await session.delete(to_delete)
                    await session.commit()
                except:
                    ...
```

```python
class DbCards(DbBase):
    
    data_model = Card

```

### AioHTTP

```python
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
        
```

```python
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
        
```

## Авторы

Александр Городецкий - г. Псков - sanyacom@mail.ru или alexandr_gorodetskiy@mail.ru

## Лицензия

Данный проект использует лицензию Apache 2.0.
Ознакомиться с лицензией можно [здесь](https://github.com/sanyacom1979/Cards_level3/blob/main/LICENSE)