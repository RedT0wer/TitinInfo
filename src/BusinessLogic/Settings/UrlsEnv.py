from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)
import os

class UrlsEnv(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="BusinessLogic/Settings/urls.env",
        extra="allow"
    )

    @classmethod
    def add_variable_to_env_file(cls, key: str, value: str, env_file: str = "BusinessLogic/Settings/urls.env"):
        if not os.path.exists(env_file):
            with open(env_file, 'w') as f:
                f.write(f"{key}={value}\n")
            return

        with open(env_file, 'r') as f:
            lines = f.readlines()

        for i, line in enumerate(lines):
            if line.startswith(key + "="):
                lines[i] = f"{key}=\'{value}\'\n"
                break
        else:
            lines.append(f"{key}=\'{value}\'\n")

        with open(env_file, 'w') as f:
            f.writelines(lines)

    @classmethod
    def remove_variable_from_env_file(cls, key: str, env_file: str = "BusinessLogic/Settings/urls.env"):
        if not os.path.exists(env_file):
            print(f"Файл {env_file} не найден.")
            return

        with open(env_file, 'r') as f:
            lines = f.readlines()

        with open(env_file, 'w') as f:
            for line in lines:
                if not line.startswith(key + "="):
                    f.write(line)