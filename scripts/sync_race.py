import asyncio

from app.database import async_session_factory
from app.services.data_loader import DataLoader


async def main():
    import sys
    if len(sys.argv) < 3:
        print("Usage: python sync_race.py <season> <round>")
        sys.exit(1)
    season = int(sys.argv[1])
    round_num = int(sys.argv[2])
    async with async_session_factory() as session:
        loader = DataLoader(session)
        await loader.sync_race(season, round_num)
        await session.commit()


if __name__ == "__main__":
    asyncio.run(main())
