import os

from fastapi.security import OAuth2PasswordBearer
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_HOST: str = os.getenv("DB_HOST")
    DB_PORT: int = os.getenv("DB_PORT")
    DB_USER: str = os.getenv("DB_USER")
    DB_PASS: str = os.getenv("DB_PASS")
    DB_NAME: str = os.getenv("DB_NAME")
    CODE_EXE_HOST: str = os.getenv("CODE_EXE_HOST")
    CODE_EXE_PORT: str = os.getenv("CODE_EXE_PORT")
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    @property
    def oauth2(self):
        return OAuth2PasswordBearer(tokenUrl="login")

    @property
    def db_url(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def code_exe_url(self):
        return f"https://{self.CODE_EXE_HOST}:{self.CODE_EXE_PORT}"


settings = Settings()
