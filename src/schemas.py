from pydantic import BaseModel


class SpreadsheetWebhookInput(BaseModel):
    username: str


class APIKey(BaseModel):
    key: str
