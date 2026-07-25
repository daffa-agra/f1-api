from fastapi import APIRouter

from app.routers import races, drivers, sessions, telemetry, circuits, teams, sync

router = APIRouter()

router.include_router(races.router)
router.include_router(drivers.router)
router.include_router(sessions.router)
router.include_router(telemetry.router)
router.include_router(circuits.router)
router.include_router(teams.router)
router.include_router(sync.router)
