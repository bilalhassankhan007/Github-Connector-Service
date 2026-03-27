import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    GITHUB_TOKEN: str = os.getenv("GITHUB_TOKEN", "").strip()
    GITHUB_API_BASE_URL: str = "https://api.github.com"
    GITHUB_API_VERSION: str = "2026-03-10"

    @classmethod
    def validate(cls) -> None:
        if not cls.GITHUB_TOKEN:
            raise RuntimeError("GITHUB_TOKEN is missing in .env file.")


settings = Settings()