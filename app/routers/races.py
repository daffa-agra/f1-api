from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

import app.database as db
from app.models.race import Race
from app.schemas.race import RaceResponse

router = APIRouter()


async def get_session() -> AsyncSession:
    async with db.async_session_factory() as session:
        yield session


@router.get("/races", response_model=list[RaceResponse])
async def list_races(
    season: int | None = None,
    circuit: str | None = None,
    page: int = Query(1, ge=1),
    per_page: int = Query(50, ge=1, le=200),
    session: AsyncSession = Depends(get_session),
):
    stmt = select(Race)
    if season is not None:
        stmt = stmt.where(Race.season == season)
    if circuit is not None:
        stmt = stmt.join(Race.circuit).where(
            Race.circuit.has(name=circuit)
        )
    stmt = stmt.order_by(Race.season.desc(), Race.round).offset((page - 1) * per_page).limit(per_page)
    result = await session.execute(stmt)
    return result.scalars().all()


@router.get("/races/{race_id}", response_model=RaceResponse)
async def get_race(race_id: int, session: AsyncSession = Depends(get_session)):
    stmt = select(Race).where(Race.race_id == race_id)
    result = await session.execute(stmt)
    race = result.scalar_one_or_none()
    if not race:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Race not found")
    return race
