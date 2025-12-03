from contextlib import asynccontextmanager

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from src.config import get_settings
from src.db.base import Base
from src.models.countrie import Country


class DBService:
    def __init__(self):
        settings = get_settings()

        self.database_url = (
            f"postgresql+asyncpg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}"
            f"@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"
        )

        self.engine = create_async_engine(self.database_url, echo=False)

        self.SessionLocal = async_sessionmaker(
            bind=self.engine,
            expire_on_commit=False,
            autocommit=False,
            autoflush=False,
            class_=AsyncSession
        )

    async def create_tables(self):
        try:
            async with self.engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
            print("✅ All tables created successfully")
        except SQLAlchemyError as e:
            print("❌ Error creating tables:", e)

    @asynccontextmanager
    async def get_session(self):
        async with self.SessionLocal() as session:
            yield session
