from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.config import settings

engine: AsyncEngine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.APP_ENV == "development",
    future=True,
    pool_pre_ping=True,
    connect_args={"ssl": "require"} if "neon" in settings.DATABASE_URL else {},
)

async_session_factory = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()
