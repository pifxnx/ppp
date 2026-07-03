from base_repository import BaseRepository
from ..models.book import Book
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func


class BookRepository(BaseRepository[Book]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Book)

    async def find_by_filters(
            self,
            title: str | None = None,
            author: str | None = None,
            genre: str | None = None,
            year: int | None = None,
            available: bool | None = None,
            limit: int = 20,
            offset: int = 0
    ) -> list[Book]:
        query = select(self.model)
        if title:
            query = query.where(self.model.title.ilike(f'%{title}%'))
        if author:
            query = query.where(self.model.author.ilike(f'%{author}%'))
        if genre:
            query = query.where(self.model.genre == genre)
        if year:
            query = query.where(self.model.year == year)
        if available is not None:
            query = query.where(self.model.available == available)
        
        query = query.limit(limit).offset(offset)
        res = await self.session.execute(query)
        res = res.scalars().all()
        return res

    async def find_by_isbn(self, isbn: str) -> Book | None:
        query = select(self.model).where(self.model.isbn == isbn)
        res = await self.session.execute(query)
        res = res.scalars().one_or_none()
        return res

    async def count_by_filters(
            self,
            title: str | None = None,
            author: str | None = None,
            genre: str | None = None,
            year: int | None = None,
            available: bool | None = None
    ) -> int:
        conditions = []
        if title:
            conditions.append(self.model.title.ilike(f'%{title}%'))
        if author:
            conditions.append(self.model.author.ilike(f'%{author}%'))
        if genre:
            conditions.append(self.model.genre == genre)
        if year:
            conditions.append(self.model.year == year)
        if available is not None:
            conditions.append(self.model.available == available)

        query = select(func.count(self.model.id)).where(*conditions)
        res = await self.session.execute(query)
        res = res.scalar()
        return res
