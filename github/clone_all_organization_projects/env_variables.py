# github/clone_all_organization_projects/env_variables.py
from pydantic_settings import BaseSettings


class MySettings(BaseSettings):
    ENVIRONMENT_NAME: str = "dev"
    GITHUB_TOKEN: str
    ORG_NAME: str
    CLONE_DIR: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


env_variables = MySettings()

GITHUB_TOKEN = env_variables.GITHUB_TOKEN
ORG_NAME = env_variables.ORG_NAME
CLONE_DIR = env_variables.CLONE_DIR
