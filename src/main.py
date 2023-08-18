import gspread
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import APIKeyQuery
from loguru import logger
from pyrogram import Client
from pyrogram.types import Message
from sqlalchemy.orm import Session
from starlette import status

import crud
from _logging import configure_logging
from db.dependency import get_session
from db.utils import create_database
from schemas import (
    SpreadsheetWebhookRequest,
    SpreadsheetWebhookResponse,
    BotUserCreate,
    BotUserUpdate,
)
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

gs = gspread.service_account(settings.GOOGLE_CREDENTIALS_FILE)


@app.on_event("startup")
async def startup():
    await create_database()
    client = userbot = Client(
        "my", in_memory=True, session_string=settings.session_string
    )
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
)
async def google_spreadsheet(
    payload: SpreadsheetWebhookRequest, db: Session = Depends(get_session)
):
    if payload.data["Выполнено"]:
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Header 'Выполнено' is true. Message already sent to telegram user",
        )
    client: Client = app.client  # noqa
    sent_messages = []
    success = None
    fail = None
    for chat_id in payload.chat_id:
        if not chat_id or chat_id == "":
            return HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"chat_id is None",
            )
        chat = await client.get_chat(chat_id)
        update_bot_user = BotUserUpdate(
            first_name=chat.first_name,
            last_name=chat.last_name,
            username=chat.username,
        )
        create_bot_user = BotUserCreate(**update_bot_user.model_dump())
        create_bot_user.id = chat.id
        bot_user = crud.bot_user.upsert(
            db,
            create=create_bot_user,
            update=update_bot_user,
            username=chat.username,
        )

        _text = "\n".join(
            list(
                map(
                    lambda x: f"<b>{x[0]}</b> - <code>{x[1]}</code>",
                    list(payload.data.items())[-5:-1],
                )
            )
        )
        b1_col = """Опишите проблему подробнее

Почему это важно?
Укажите факты, которые подтверждают необходимость подсветки.
УТП или другие детали."""
        text = (
            f"Ответ по Вашей проблеме\n<code>{payload.data[b1_col]}</code>\n\n{_text}"
        )
        if bot_user.is_notified:
            um = await client.edit_message_text(
                bot_user.username, bot_user.message_id, text=text
            )
            update_bot_user2 = BotUserUpdate(is_notified=True, message_id=um.id)
            bot_user = crud.bot_user.upsert(
                db, update=update_bot_user2, username=chat.username
            )
            return HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Header 'Выполнено' is true. Message already sent to telegram user",
            )

        m: Message = await client.send_message(
            chat_id,
            text,
        )
        sent_messages.append(m.id)
        update_bot_user3 = BotUserUpdate(is_notified=True, message_id=m.id)
        bot_user = crud.bot_user.upsert(
            db, update=update_bot_user3, username=chat.username
        )
    if len(payload.chat_id) == len(sent_messages):
        success = len(payload.chat_id)
    else:
        fail = abs(len(payload.chat_id) - len(sent_messages))
    response = SpreadsheetWebhookResponse(
        message_ids=sent_messages, success=success, fail=fail
    )
    return response
