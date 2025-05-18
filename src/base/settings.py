import os

from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

dotenv_path = os.path.join(BASE_DIR, '.env')

if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

DEBUG = bool(os.environ.get("DEBUG", False))

# db
POSTGRES_USER = os.environ.get("POSTGRES_USER")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
POSTGRES_DB_NAME = os.environ.get("POSTGRES_DB_NAME")
POSTGRES_DB = os.environ.get("POSTGRES_DB", "db")
SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@" \
                          f"{POSTGRES_DB}/{POSTGRES_DB_NAME}"
ALLOW_ORIGINS = os.environ.get("ALLOW_ORIGINS").split(",")
