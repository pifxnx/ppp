from typing import Generic, TypeVar
from pydantic import BaseModel, Field


T = TypeVar('T')

class PaginationParams(BaseModel):
    '''параметры пагинации'''
    page: int = Field(1, ge=1, description='номер страницы')
    page_size: int = Field(20, ge=1, le=100, description='размер страницы')

    @property
    def offset(self) -> int:
        '''вычислить offset для sql'''
        return (self.page - 1) * self.page_size
    
    @property
    def limit(self) -> int:
        '''limit для sql'''
        return self.page_size
    

class PaginatedResponse(BaseModel, Generic[T]):
    '''generic схема для пагинированных ответов'''
    items: list[T]
    total: int = Field(..., description='всего элементов')
    page: int = Field(..., description='текущая страница')
    page_size: int = Field(..., description='размер страницы')
    pages: int = Field(..., description='всего страниц')

    @classmethod
    def create(
        cls,
        items: list[T],
        total: int,
        pagination: PaginationParams
    ):
        '''создать пагинированный ответ'''
        pages = (total + pagination.page_size - 1) // pagination.page_size

        return cls(
            items=items,
            total=total,
            page=pagination.page,
            page_size=pagination.page_size,
            pages=pages
        )
    

class HealthCheckResponse(BaseModel):
    '''схема для health check'''
    status: str = 'healthy'
    database: str = 'connected'