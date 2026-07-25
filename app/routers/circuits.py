from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.database import async_session_factory
from app.models.circuit import Circuit
from app.schemas.circuit import CircuitResponse

router = APIRouter()


async def get_session() -> AsyncSession:
    async with async_session_factory() as session:
        yield session


@router.get("/circuits", response_model=list[CircuitResponse])
async def list_circuits(
    country: str | None = None,
    page: int = Query(1, ge=1),
    per_page: int = Query(50, ge=1, le=200),
    db: AsyncSession = Depends(get_session),
):
    stmt = select(Circuit)
    if country is not None:
        stmt = stmt.where(Circuit.country == country)
    stmt = stmt.order_by(Circuit.name).offset((page - 1) * per_page).limit(per_page)
    result = await db.execute(stmt)
    return result.scalars().all()
