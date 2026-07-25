from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from app.database import async_session_factory
from app.models.telemetry import Telemetry
from app.schemas.telemetry import TelemetryResponse

router = APIRouter()


async def get_session() -> AsyncSession:
    async with async_session_factory() as session:
        yield session


@router.get("/sessions/{session_id}/telemetry", response_model=list[TelemetryResponse])
async def get_session_telemetry(
    session_id: int,
    driver_id: int | None = None,
    lap_id: int | None = None,
    page: int = Query(1, ge=1),
    per_page: int = Query(200, ge=1, le=1000),
    db: AsyncSession = Depends(get_session),
):
    stmt = select(Telemetry).where(Telemetry.session_id == session_id)
    if driver_id is not None:
        stmt = stmt.where(Telemetry.driver_id == driver_id)
    if lap_id is not None:
        stmt = stmt.where(Telemetry.lap_id == lap_id)
    stmt = stmt.order_by(Telemetry.timestamp).offset((page - 1) * per_page).limit(per_page)
    result = await db.execute(stmt)
    return result.scalars().all()


@router.get("/drivers/{driver_id}/telemetry", response_model=list[TelemetryResponse])
async def get_driver_telemetry(
    driver_id: int,
    session_id: int | None = None,
    lap_id: int | None = None,
    page: int = Query(1, ge=1),
    per_page: int = Query(200, ge=1, le=1000),
    db: AsyncSession = Depends(get_session),
):
    stmt = select(Telemetry).where(Telemetry.driver_id == driver_id)
    if session_id is not None:
        stmt = stmt.where(Telemetry.session_id == session_id)
    if lap_id is not None:
        stmt = stmt.where(Telemetry.lap_id == lap_id)
    stmt = stmt.order_by(Telemetry.timestamp).offset((page - 1) * per_page).limit(per_page)
    result = await db.execute(stmt)
    return result.scalars().all()
