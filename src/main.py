import asyncio

from fastapi import FastAPI, Depends

from _logging import configure_logging
from schemas import SpreadsheetWebhookInput
from security import verify_api_key
from settings import settings
from userbot import create_userbot

configure_logging()

app = FastAPI(dependencies=[Depends(verify_api_key)])
client = asyncio.run(create_userbot(
    settings.PROJECT_NAME,
    api_id=settings.API_ID,
    api_hash=settings.API_HASH,
    phone_number=settings.PHONE_NUMBER,
))


@app.post('/send_message')
async def google_spreadsheet_webhook(data: SpreadsheetWebhookInput):
    client.send_message("")
