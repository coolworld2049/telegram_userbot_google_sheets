from typing import Optional

from loguru import logger
from sqlalchemy.orm import Session

from crud.base import CRUDBase, ModelType
from db import models
from schemas.bot_user import BotUserUpdate, BotUserCreate


class CRUDBotUser(CRUDBase[models.BotUser, BotUserCreate, BotUserUpdate]):
    def get_by_username(self, db: Session, username: str) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.username == username).first()

    def upsert(
        self,
        db,
        create: BotUserCreate | None = None,
        *,
        update: BotUserUpdate,
        username: str
    ) -> models.BotUser:
        bot_user = self.get_by_username(db, username=username)
        try:
            if not bot_user:
                bot_user = self.create(db, obj_in=create)
            else:
                bot_user = self.update(db, db_obj=bot_user, obj_in=update)
        except Exception as e:
            logger.error(e)
        return bot_user


bot_user = CRUDBotUser(models.BotUser)
