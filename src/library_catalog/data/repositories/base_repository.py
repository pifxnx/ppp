from typing import Generic, TypeVar, Type
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update


T = TypeVar('T')

class BaseRepository(Generic[T]):
    def __init__(self, session: AsyncSession, model: Type[T]):
        self.session = session
        self.model = model

    async def create(self, **kwargs) -> T:
        obj = self.model(**kwargs)
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj


    async def get_by_id(self, id: UUID) -> T | None:
        obj = await self.session.get(self.model, id)
        return obj

    async def update(self, id: UUID, **kwargs) -> T | None:
        obj = await self.session.get(self.model, id)
        if not obj:
            return None
        
        for k, v in kwargs.items():
            setattr(obj, k, v)
        
        # query = (
        #     update(self.model).
        #     where(self.model.id == id).
        #     values(**kwargs)
        # )
        # await self.session.execute(query)
        await self.session.commit()
        return obj
        

    async def delete(self, id: UUID) -> bool:
        obj = await self.session.get(self.model, id)
        if not obj:
            return False
        
        # stmt = delete(self.model).where(self.model.id == id)
        # await self.session.execute(stmt)
        await self.session.delete(obj)
        await self.session.commit()
        return True
        

    async def get_all(
            self,
            limit: int = 100,
            offset: int = 0
    ) -> list[T]:
        query = select(self.model).limit(limit).offset(offset)
        res = await self.session.execute(query)
        res = res.scalars().all()
        return res
    

