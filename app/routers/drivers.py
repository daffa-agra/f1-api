from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

import app.database as db
from app.models.driver import Driver
from app.schemas.driver import DriverResponse

router = APIRouter()


async def get_session() -> AsyncSession:
    async with db.async_session_factory() as session:
        yield session


@router.get("/drivers", response_model=list[DriverResponse])
async def list_drivers(
    season: int | None = None,
    team: str | None = None,
    page: int = Query(1, ge=1),
    per_page: int = Query(50, ge=1, le=200),
    session: AsyncSession = Depends(get_session),
):
    stmt = select(Driver)
    if team is not None:
        stmt = stmt.where(Driver.team == team)
    stmt = stmt.order_by(Driver.name).offset((page - 1) * per_page).limit(per_page)
    result = await session.execute(stmt)
    return result.scalars().all()


@router.get("/drivers/{driver_id}", response_model=DriverResponse)
async def get_driver(driver_id: int, session: AsyncSession = Depends(get_session)):
    stmt = select(Driver).where(Driver.driver_id == driver_id)
    result = await session.execute(stmt)
    driver = result.scalar_one_or_none()
    if not driver:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Driver not found")
    return driver
