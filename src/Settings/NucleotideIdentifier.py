from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, create_model

class InitialModel(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="Settings/nucleotide_identifier.env",
        env_file_encoding="utf-8",
        extra="allow"
    )

initialModel = InitialModel()
env_vars = initialModel.model_dump()
fields = {k: (str, Field(default=v)) for k, v in env_vars.items()}
NucleotideIdentifier = create_model("NucleotideIdentifier", **fields, __base__=BaseSettings)
nucleotideIdentifier = NucleotideIdentifier()