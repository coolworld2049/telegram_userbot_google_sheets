from loguru import logger
from pyrogram import Client

from src.settings import settings


async def create_userbot(name="userbot", *, api_id, api_hash, phone_number, **kwargs):
    try:
        if not api_id or not api_hash or not phone_number:
            raise ValueError("API credentials and phone number are required")
        userbot = Client(
            name, api_id=api_id, api_hash=api_hash, phone_number=phone_number, **kwargs
        )
        await userbot.start()
        logger.info("Userbot started")
        return userbot
    except Exception as e:
        logger.error(e)
        return None
