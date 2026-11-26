import os

os.environ["DB_HOST"] = "127.0.0.1"
os.environ["DB_NAME"] = "urlshort_test"

import pytest

from app.config import DB_NAME
from app.storage import get_connection, init_db


@pytest.fixture(autouse=True)
def clean_links():
    assert DB_NAME.endswith("_test"), f"refusing to truncate {DB_NAME}"
    init_db()
    with get_connection() as conn:
        conn.execute("TRUNCATE TABLE links")
    yield
