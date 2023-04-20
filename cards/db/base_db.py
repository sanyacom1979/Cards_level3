from sqlalchemy.ext.asyncio import AsyncSession


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