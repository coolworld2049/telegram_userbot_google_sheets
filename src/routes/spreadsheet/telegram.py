from fastapi import HTTPException, APIRouter
from loguru import logger
from pyrogram import Client
from pyrogram.types import Message
from starlette import status
from starlette.requests import Request

from schemas import SpreadsheetRequest, SpreadsheetResponse
from template_engine import render_template

router = APIRouter(prefix="/telegram", tags=["spreadsheet updates"])


@router.post(
    "/send_message",
)
async def google_spreadsheet(request: Request, payload: SpreadsheetRequest):
    client: Client = request.app.client
    if not payload.chat_id or payload.chat_id == "":
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"chat_id must not be empty",
        )
    chat = await client.get_chat(payload.chat_id)
    response = SpreadsheetResponse(message_id=payload.message_id)
    await client.delete_messages(payload.chat_id, payload.data["message_id"])
    m: Message = await client.send_message(
        payload.chat_id,
        render_template(
            "notification.html",
            items=list(payload.data.items())[
                payload.notification_message_column_range[
                    0
                ] : payload.notification_message_column_range[1]
            ],
            user_problem_data=payload.data[payload.user_problem_column_name],
        ),
    )
    response.is_notified = True
    response.message_id = m.id
    logger.info(f"Sent message: {m.__dict__}")
    return response
