from pydantic import BaseModel


class SpreadsheetBase(BaseModel):
    message_id: int | None = None
    is_notified: bool = False


class SpreadsheetRequest(SpreadsheetBase):
    chat_id: int | str
    data: dict
    event: dict | None = None
    user_problem_column_name: str
    notification_message_column_range: list[int]


class SpreadsheetResponse(SpreadsheetBase):
    content: str | None = None
