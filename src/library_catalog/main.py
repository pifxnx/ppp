from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

from .core.config import settings
from .core.database import dispose_engine
from .core.exceptions import register_exception_handlers
from .core.logging_config import setup_logging
from .api.v1.routers import books, health


@asynccontextmanager
async def lifespan(app: FastAPI):
    '''
    lifecycle manager для FastAPI
    Выполняется при: startup (настрока логирования),
    shutdown (закрытие подключений к бд)
    '''
    setup_logging()
    print('Application started')

    yield

    await dispose_engine()
    print('Application stopped')


app = FastAPI(
    title=settings.app_name,
    description='REST API для управленя библиотечным каталогом',
    version='1.0.0',
    docs_url=settings.docs_url,
    redoc_url=settings.redoc_url,
    lifespan=lifespan
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

register_exception_handlers(app)


app.include_router(
    books.router,
    prefix=settings.api_v1_prefix
)
app.include_router(
    health.router,
    prefix=settings.api_v1_prefix
)

@app.get('/')
async def root():
    '''Корневой эндпоинт'''
    return {
        'message': 'Welcome to Library Catalog API',
        'docs': settings.docs_url,
        'version': '1.0.0'
    }
    


@app.get('/health')
async def health_check():
    '''Health check endpoint'''
    return {'status': 'healthy'}


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)