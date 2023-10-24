from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    app_id: str = Field(validation_alias="APPID")
    api_key: str = Field(validation_alias="APIKey")
    api_secret: str = Field(validation_alias="APISecret")
    api_url: str

    model_config = SettingsConfigDict(env_file=".env")
