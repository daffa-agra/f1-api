from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

import app.database as db
from app.models.team import Team
from app.schemas.team import TeamResponse

router = APIRouter()


async def get_session() -> AsyncSession:
    async with db.async_session_factory() as session:
        yield session


@router.get("/teams", response_model=list[TeamResponse])
async def list_teams(
    nationality: str | None = None,
    page: int = Query(1, ge=1),
    per_page: int = Query(50, ge=1, le=200),
    db: AsyncSession = Depends(get_session),
):
    stmt = select(Team)
    if nationality is not None:
        stmt = stmt.where(Team.nationality == nationality)
    stmt = stmt.order_by(Team.name).offset((page - 1) * per_page).limit(per_page)
    result = await db.execute(stmt)
    return result.scalars().all()
