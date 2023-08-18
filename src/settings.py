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
    SESSION_STRING_FILE: str = "src/session_maker/my.txt"
    API_KEY_FILE: str = str(pathlib.Path(__file__).parent.parent / "api_key.txt")

    @property
    def session_string(self):
        return pathlib.Path(self.SESSION_STRING_FILE).open("r").readline()

    @property
    def api_key(self):
        return pathlib.Path(self.API_KEY_FILE).open("r").readline().replace("\n", "")


class Settings(UserBotSettings):
    PROJECT_NAME: Optional[str] = "TelegramUserbotGoogleSheets"
    LOGGING_LEVEL: Optional[str] = "INFO"

    class Config:
        case_sensitive = True


settings = Settings()
