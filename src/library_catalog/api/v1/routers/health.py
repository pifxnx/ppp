from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from ..schemas.common import HealthCheckResponse
from ...dependencies import DbSessionDep

router = APIRouter(prefix="/health", tags=["Health"])


@router.get(
    "/",
    response_model=HealthCheckResponse,
    summary="Health Check",
    description="Проверить состояние сервиса и подключения к бд",
)
async def health_check(db: DbSessionDep):
    """
    Проверить здоровье сервиса.
    Проверяет: сервис запущен, подключение к бд работает
    """
    # Просто запрос к бд
    try:
        await db.execute(text("SELECT 1"))
        db_status = "connected"

    except Exception:
        db_status = "disconnected"

    return HealthCheckResponse(status="healthy", database=db_status)

