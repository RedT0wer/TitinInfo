from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)

class UrlsEnv(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="BusinessLogic/Settings/urls.env",
        extra="allow"
    )

urlsEnv = UrlsEnv()