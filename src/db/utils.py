from sqlalchemy import text

from db.base import Base
from db.session import engine
from settings import settings


async def create_database():
    Base.metadata.create_all(engine)


async def drop_database() -> None:
    async with engine.connect() as conn:
        disc_users = (
            "SELECT pg_terminate_backend(pg_stat_activity.pid) "
            "FROM pg_stat_activity "
            f"WHERE pg_stat_activity.datname = '{settings.DATABASE_URL}' "
            "AND pid <> pg_backend_pid();"
        )
        await conn.execute(text(disc_users))
        await conn.execute(text(f'DROP DATABASE "{settings.DATABASE_URL}"'))