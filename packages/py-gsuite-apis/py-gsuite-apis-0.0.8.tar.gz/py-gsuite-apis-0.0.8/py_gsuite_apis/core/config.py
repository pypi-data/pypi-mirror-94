from functools import lru_cache

from pydantic import BaseSettings


class GoogleApiSettings(BaseSettings):
    SCOPE: str
    BUILD: str
    VERSION: str


class GoogleSettings(BaseSettings):
    SLIDES: GoogleApiSettings = GoogleApiSettings(
        SCOPE="https://www.googleapis.com/auth/presentations",
        BUILD="slides",
        VERSION="v1",
    )
    DRIVE: GoogleApiSettings = GoogleApiSettings(
        SCOPE="https://www.googleapis.com/auth/drive",
        BUILD="drive",
        VERSION="v3",
    )
    SHEETS: GoogleApiSettings = GoogleApiSettings(
        SCOPE="https://www.googleapis.com/auth/spreadsheets",
        BUILD="sheets",
        VERSION="v4",
    )


class PyGsuiteApisSettings(GoogleSettings):
    pass


@lru_cache()
def get_config() -> PyGsuiteApisSettings:
    return PyGsuiteApisSettings()
