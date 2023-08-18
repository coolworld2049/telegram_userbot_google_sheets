from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class BotUserBase(BaseModel):
    id: Optional[int] | None = None
    first_name: Optional[str] | None = None
    last_name: Optional[str] | None = None
    username: Optional[str] | None = None
    is_notified: Optional[bool] | None = False
    message_id: Optional[int] | None = None


class BotUserCreate(BotUserBase):
    pass


class BotUserUpdate(BotUserBase):
    pass


class BotUser(BotUserBase):
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True
