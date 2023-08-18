from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import APIKeyQuery
from loguru import logger
from pyrogram import Client, idle
from starlette import status

from _logging import configure_logging
from routes.spreadsheet import telegram
from settings import settings

configure_logging()

api_key = APIKeyQuery(name="api_key")


async def verify_api_key(key: str = Depends(api_key)):
    if key != settings.api_key:
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
    app.include_router(telegram.router)
    client = userbot = Client(
        "my", in_memory=True, session_string=settings.session_string
    )
    if not client:
        raise ValueError(client)
    await userbot.start()
    app.client = client
    logger.info(f"userbot started. Client idle")
    logger.info("Application started")


@app.on_event("shutdown")
async def shutdown():
    await app.client.stop()  # noqa
    logger.info("Application shutdown")
