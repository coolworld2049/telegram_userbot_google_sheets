from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import APIKeyQuery
from loguru import logger
from pyrogram import Client
from pyrogram.types import Message
from starlette import status

from _logging import configure_logging
from schemas import SpreadsheetWebhookRequest, SpreadsheetWebhookResponse
from settings import settings

configure_logging()

api_key = APIKeyQuery(name="api_key")


async def verify_api_key(key: str = Depends(api_key)):
    if key != settings.API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
        )


app = FastAPI(
    title=settings.PROJECT_NAME,
    dependencies=[Depends(verify_api_key)],
)


@app.on_event("startup")
async def startup():
    client = userbot = Client("my", in_memory=True, session_string=settings.session_string)
    await userbot.start()
    if not client:
        raise ValueError(client)
    app.client = client
    logger.info(f"Userbot started")
    logger.info("Application started")


@app.on_event("shutdown")
async def shutdown():
    logger.info("Application shutdown")


@app.post(
    "/telegram/send_message",
    tags=["telegram"],
    response_model=SpreadsheetWebhookResponse,
)
async def google_spreadsheet_webhook(data: SpreadsheetWebhookRequest):
    client: Client = app.client  # noqa
    sent_messages = []
    success = None
    fail = None
    for chat_id in data.chat_id:
        m: Message = await client.send_message(
            chat_id, data.text, parse_mode=data.parse_mode
        )
        sent_messages.append(m.id)
    if len(data.chat_id) == len(sent_messages):
        success = len(data.chat_id)
    else:
        fail = abs(len(data.chat_id) - len(sent_messages))
    response = SpreadsheetWebhookResponse(
        message_ids=sent_messages, success=success, fail=fail
    )
    return response
