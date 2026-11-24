import os

BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:8000")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
DB_NAME = os.getenv("DB_NAME", "urlshort")
DB_USER = os.getenv("DB_USER", "urlshort")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
