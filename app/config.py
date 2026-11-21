import os

BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:8000")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
