from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.services.data_loader import DataLoader


def init_scheduler(db_factory):
    scheduler = AsyncIOScheduler()

    async def daily_sync_job():
        async with db_factory() as db:
            loader = DataLoader(db)
            await loader.sync_all_2026()
            await db.commit()

    scheduler.add_job(daily_sync_job, "cron", hour=6, minute=0)
    return scheduler
