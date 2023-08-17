
from loguru import logger
from pyrogram import Client, errors


async def create_userbot(name="userbot", *, api_id, api_hash, phone_number, **kwargs):
    try:
        if not api_id or not api_hash or not phone_number:
            raise ValueError("API credentials and phone number are required")
        userbot = Client(name, api_id=api_id, api_hash=api_hash, **kwargs)
        try:
            await userbot.start()
        except (
            errors.ActiveUserRequired,
            errors.AuthKeyInvalid,
            errors.AuthKeyPermEmpty,
            errors.AuthKeyUnregistered,
            errors.AuthKeyDuplicated,
            errors.SessionExpired,
            errors.SessionPasswordNeeded,
            errors.SessionRevoked,
            errors.UserDeactivated,
            errors.UserDeactivatedBan,
        ) as e:
            logger.error(e)
            sent_code_info = await userbot.send_code(phone_number)
            phone_code = input("Please enter your phone code: ")
            await userbot.sign_in(
                phone_number, sent_code_info.phone_code_hash, phone_code
            )
        else:
            logger.info("Login successfully")
        return userbot
    except Exception as e:
        logger.exception(e)
        return None
