from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import async_session_factory
from app.models.session import Session
from app.models.lap import Lap
from app.models.pit_stop import PitStop
from app.schemas.session import SessionResponse
from app.schemas.lap import LapResponse
from app.schemas.pit_stop import PitStopResponse

router = APIRouter()


async def get_session() -> AsyncSession:
    async with async_session_factory() as session:
        yield session


@router.get("/sessions/{session_id}", response_model=SessionResponse)
async def get_session_detail(session_id: int, db: AsyncSession = Depends(get_session)):
    stmt = select(Session).where(Session.session_id == session_id)
    result = await db.execute(stmt)
    s = result.scalar_one_or_none()
    if not s:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Session not found")
    return s


@router.get("/sessions/{session_id}/laps", response_model=list[LapResponse])
async def list_session_laps(
    session_id: int,
    driver_id: int | None = None,
    page: int = Query(1, ge=1),
    per_page: int = Query(50, ge=1, le=200),
    db: AsyncSession = Depends(get_session),
):
    stmt = select(Lap).where(Lap.session_id == session_id)
    if driver_id is not None:
        stmt = stmt.where(Lap.driver_id == driver_id)
    stmt = stmt.order_by(Lap.lap_number).offset((page - 1) * per_page).limit(per_page)
    result = await db.execute(stmt)
    return result.scalars().all()


@router.get("/sessions/{session_id}/results", response_model=list[LapResponse])
async def session_results(
    session_id: int,
    db: AsyncSession = Depends(get_session),
):
    stmt = select(Lap).where(Lap.session_id == session_id).order_by(Lap.lap_number)
    result = await db.execute(stmt)
    return result.scalars().all()


@router.get("/sessions/{session_id}/pitstops", response_model=list[PitStopResponse])
async def session_pitstops(
    session_id: int,
    driver_id: int | None = None,
    db: AsyncSession = Depends(get_session),
):
    stmt = select(PitStop).where(PitStop.session_id == session_id)
    if driver_id is not None:
        stmt = stmt.where(PitStop.driver_id == driver_id)
    result = await db.execute(stmt)
    return result.scalars().all()
