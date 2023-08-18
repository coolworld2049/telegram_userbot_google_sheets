from sqlalchemy import Column, BigInteger, String, Boolean

from db import Base
from db.base import TimestampsMixin


class BotUser(Base, TimestampsMixin):
    id = Column(BigInteger, primary_key=True, autoincrement=False)
    first_name = Column(String)
    last_name = Column(String)
    username = Column(String, unique=True)
    is_notified = Column(Boolean)
    message_id = Column(BigInteger)
