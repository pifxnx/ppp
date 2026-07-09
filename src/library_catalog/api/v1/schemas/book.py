from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field, field_validator


class BookBase(BaseModel):
    '''базовая схема с общими полями'''
    title: str = Field(..., min_length=1, max_length=500)
    author: str = Field(..., min_length=1, max_length=300)
    year: int = Field(..., ge=1000, le=2100)
    genre: str = Field(..., min_length=1, max_length=100)
    pages: int = Field(..., gt=0)


class BookCreate(BookBase):
    '''схема для создания книги'''
    isbn: str | None = Field(None, min_length=10, max_length=500)
    description: str | None = Field(None, max_length=5000)

    @field_validator('isbn')
    @classmethod
    def validate_isbn(cls, v: str | None) -> str | None:
        '''валидация isbn'''
        if v is None:
            return v
        
        clean = v.replace('-', '').replace(' ', '')
        
        if not clean.replace('X', '').isdigit():
            raise ValueError('isbn must contain only digits')
        
        if len(clean) not in (10, 13):
            raise ValueError('isbn must be 10 or 13 digits')
        
        return v
    
    model_config = {
        'json_schema_extra': {
            'examples': [
                {
                    'title': 'Clean Code',
                    'author': 'Robert Martin',
                    'year': 2008,
                    'genre': 'Programming',
                    'pages': 464,
                    'isbn': '978-0132350884',
                    'description': 'A Handbook of Agile Sorftware Craftsmanship'
                }
            ]
        }
    }


class BookUpdate(BaseModel):
    '''схема для обновления книги'''
    title: str | None = Field(None, min_length=1, max_length=500)
    author: str | None = Field(None, min_length=1, max_length=300)
    year: int | None = Field(None, ge=1000, le=2100)
    genre: str | None = Field(None, min_length=1, max_length=100)
    pages: int | None = Field(None, gt=0)
    available: bool | None = None
    isbn: str | None = None
    description: str | None = None

    @field_validator('isbn')
    @classmethod
    def validate_isbn(cls, v: str | None) -> str | None:
        '''валидация isbn'''
        if v is None:
            return v
        
        clean = v.replace('-', '').replace(' ', '')
        
        if not clean.replace('X', '').isdigit():
            raise ValueError('isbn must contain only digits')
        
        if len(clean) not in (10, 13):
            raise ValueError('isbn must be 10 or 13 digits')
        
        return v



class ShowBook(BookBase):
    '''схема для отображения книги (response)'''
    book_id: UUID
    available: bool
    isbn: str | None
    description: str | None
    extra: dict | None
    created_at: datetime
    updated_at: datetime

    model_config = {
        'from_attributes': True,
        'json_schema_extra': {
            'examples': [
                {
                    "book_id": "123e4567-e89b-12d3-a456-426614174000",
                    "title": "Clean Code",
                    "author": "Robert Martin",
                    "year": 2008,
                    "genre": "Programming",
                    "pages": 464,
                    "available": True,
                    "isbn": "978-0132350884",
                    "description": "A Handbook of Agile Software Craftsmanship",
                    "extra": {
                        "cover_url": "https://covers.openlibrary.org/b/id/123-L.jpg",
                        "subjects": ["Computer Science", "Software Engineering"]
                    },
                    'created_at': '2024-01-01T12:00:00',
                    'updated_at': '2024-01-01T12:00:00'
                }
            ]
        }
    }


class BookFilters(BaseModel):
    '''фильтры для поиска книг'''
    title: str | None = Field(None, description='Поиск по названию (частичное совпадение)')
    author: str | None = Field(None, description='поиск по автору (частичное совпадение)')
    genre: str | None = Field(None, description='точное совпадение жанра')
    year: int | None = Field(None, description='точное совпадение года')
    available: bool | None = Field(None, description='фильтр по доступности')
    