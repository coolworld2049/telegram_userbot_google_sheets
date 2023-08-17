import logging
import os
import pathlib
from typing import Optional

from dotenv import load_dotenv, find_dotenv
from pydantic_settings import BaseSettings

project_path = pathlib.Path(__file__).parent.parent


class BaseAppSettings(BaseSettings):
    load_dotenv(find_dotenv(f"{project_path}/.env"))
    stage_dotenv: str = find_dotenv(f'{project_path}/.env.{os.getenv("STAGE", "dev")}')
    load_dotenv(stage_dotenv, override=True) if stage_dotenv else None


class UserBotSettings(BaseAppSettings):
    API_ID: int
    API_HASH: str
    PHONE_NUMBER: str
    API_KEY: str


class Settings(UserBotSettings):
    PROJECT_NAME: Optional[str] = "telegram_userbot_google_sheets"
    LOGGING_LEVEL: Optional[str | int] = logging.getLevelName(
        os.getenv("LOGGING_LEVEL", "INFO")
    )

    class Config:
        case_sensitive = True


settings = Settings()
