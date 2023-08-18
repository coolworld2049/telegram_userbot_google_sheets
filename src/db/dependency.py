from loguru import logger
from sqlalchemy import exc
from sqlalchemy.ext.asyncio import AsyncSession

from db.session import SessionLocal


def get_session() -> AsyncSession:
    s = SessionLocal()
    try:
        yield s
    except (
        exc.SQLAlchemyError,
        exc.IntegrityError,
        exc.PendingRollbackError,
    ) as e:  # noqa
        s.rollback()
        logger.debug(f"{e.__class__} {e} - ROLLBACK")
    finally:
        s.close()
