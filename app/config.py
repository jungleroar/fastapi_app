import os
from typing import Literal

from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Settings(object):
    DB_HOST: str = os.environ.get("DB_HOST")
    DB_PORT: int = os.environ.get("DB_PORT")
    DB_USER: str = os.environ.get("DB_USER")
    DB_PASS: str = os.environ.get("DB_PASS")
    DB_NAME: str = os.environ.get("DB_NAME")
    DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    TEST_DB_HOST: str = os.environ.get("TEST_DB_HOST")
    TEST_DB_PORT: int = os.environ.get("TEST_DB_PORT")
    TEST_DB_USER: str = os.environ.get("TEST_DB_USER")
    TEST_DB_PASS: str = os.environ.get("TEST_DB_PASS")
    TEST_DB_NAME: str = os.environ.get("TEST_DB_NAME")
    TEST_DATABASE_URL = f"postgresql+asyncpg://{TEST_DB_USER}:{TEST_DB_PASS}@{TEST_DB_HOST}:{TEST_DB_PORT}/{TEST_DB_NAME}"
    
    SECRET_KEY: str = os.environ.get("SECRET_KEY")
    ALGORITHM: str = os.environ.get("ALGORITHM")

    SMTP_HOST: str = os.environ.get("SMTP_HOST")
    SMTP_PORT: int = os.environ.get("SMTP_PORT")
    SMTP_USER: str = os.environ.get("SMTP_USER")
    SMTP_PASS: str = os.environ.get("SMTP_PASS")

    MODE: Literal["DEV", "TEST", "PROD"] = "DEV"


settings = Settings()
