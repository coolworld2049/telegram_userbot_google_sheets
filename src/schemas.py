from typing import Any

from pydantic import BaseModel


class SpreadsheetWebhookRequest(BaseModel):
    chat_id: list[Any]
    data: dict


class SpreadsheetWebhookResponse(BaseModel):
    message_ids: list[int]
    success: int | None
    fail: int | None


class APIKey(BaseModel):
    key: str
