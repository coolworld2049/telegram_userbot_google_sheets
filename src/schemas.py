from typing import Any

from pydantic import BaseModel
from pyrogram.enums import ParseMode


class SpreadsheetWebhookRequest(BaseModel):
    chat_id: list[Any]
    text: str
    parse_mode: ParseMode | None = ParseMode.HTML


class SpreadsheetWebhookResponse(BaseModel):
    message_ids: list[int]
    success: int | None
    fail: int | None


class APIKey(BaseModel):
    key: str
