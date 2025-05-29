from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)

class Settings(BaseSettings):
    find: str
    insert: str
    replacement: str
    delete_nucleotide: str
    delete_exon: str
    model_config = SettingsConfigDict(
        env_file="BusinessLogic/Settings/.env"
    )

settings = Settings()