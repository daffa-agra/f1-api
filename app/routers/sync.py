from fastapi import APIRouter, Depends, Header, HTTPException

import app.database as db
from app.services.data_loader import DataLoader

router = APIRouter()


async def get_session():
    async with db.async_session_factory() as session:
        yield session


@router.post("/sync/races")
async def sync_race(
    season: int,
    round_num: int,
    x_sync_token: str | None = Header(default=None),
    session=Depends(get_session),
):
    from app.config import settings
    if settings.SYNC_TOKEN and x_sync_token != settings.SYNC_TOKEN:
        raise HTTPException(status_code=403, detail="Invalid sync token")
    loader = DataLoader(session)
    await loader.sync_race(season, round_num)
    await session.commit()
    return {"status": "ok", "message": f"Synced season={season} round={round_num}"}


@router.post("/sync/all")
async def sync_all(
    x_sync_token: str | None = Header(default=None),
    session=Depends(get_session),
):
    from app.config import settings
    if settings.SYNC_TOKEN and x_sync_token != settings.SYNC_TOKEN:
        raise HTTPException(status_code=403, detail="Invalid sync token")
    loader = DataLoader(session)
    await loader.sync_all_2026()
    await session.commit()
    return {"status": "ok", "message": "Synced all available 2026 data"}
