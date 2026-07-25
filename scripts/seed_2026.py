import asyncio

from app.database import async_session_factory
from app.services.data_loader import DataLoader


async def main():
    async with async_session_factory() as session:
        loader = DataLoader(session)
        await loader.sync_all_2026()
        await session.commit()


if __name__ == "__main__":
    asyncio.run(main())
