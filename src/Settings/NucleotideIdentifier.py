from pydantic_settings import BaseSettings, SettingsConfigDict

class NucleotideIdentifier(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="nucleotide_identifier.env",
        env_file_encoding="utf-8",
        extra="allow"
    )
nucleotideIdentifier = NucleotideIdentifier()
print(nucleotideIdentifier.model_dump())