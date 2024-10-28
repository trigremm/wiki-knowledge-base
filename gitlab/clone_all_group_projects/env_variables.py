# fastapi_backend/oraclus_netflow/configs/env_settings.py
from pydantic_settings import BaseSettings


class MySettings(BaseSettings):
    ENVIRONMENT_NAME: str = "dev"
    ACCESS_TOKEN: str
    GROUP_ID: str
    CLONE_DIR: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


env_variables = MySettings()

ACCESS_TOKEN = env_variables.ACCESS_TOKEN
GROUP_ID = env_variables.GROUP_ID
CLONE_DIR = env_variables.CLONE_DIR
