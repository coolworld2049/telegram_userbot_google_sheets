from contextlib import contextmanager

from loguru import logger
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from settings import settings

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


@contextmanager
def get_db() -> SessionLocal:
    s = SessionLocal()
    try:
        yield s
        s.commit()
    except Exception as e:
        logger.debug(f"{e.__class__} {e} - ROLLBACK")
        s.rollback()
        raise e
    finally:
        s.close()
