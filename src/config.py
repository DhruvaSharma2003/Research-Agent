import os
from dotenv import load_dotenv

# Load .env for local development (if present)
load_dotenv()

def get_env(key: str, default: str | None = None) -> str | None:
    return os.getenv(key, default)

OPENAI_API_KEY = get_env("OPENAI_API_KEY")
TAVILY_API_KEY = get_env("TAVILY_API_KEY")

GOOGLE_CLIENT_ID = get_env("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = get_env("GOOGLE_CLIENT_SECRET")
GOOGLE_OAUTH_REDIRECT_URI = get_env("GOOGLE_OAUTH_REDIRECT_URI")

GOOGLE_DRIVE_REPORTS_FOLDER_NAME = get_env(
    "GOOGLE_DRIVE_REPORTS_FOLDER_NAME",
    "Research-Agent Reports",
)
