import logging

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()
logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    PROJECT_NAME: str
    ALLOW_ORIGINS: list = ["*"]
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000
    APP_RELOAD: bool = False

    API_V1_STR: str = "/api/v1"

    GITHUB_API_URL: str


settings = Settings()
