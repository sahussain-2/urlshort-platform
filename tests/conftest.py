import os

os.environ["DB_HOST"] = "127.0.0.1"
os.environ["DB_NAME"] = "urlshort_test"

import pytest  # noqa: E402

from app.storage import get_connection  # noqa: E402


@pytest.fixture(autouse=True)
def clean_links():
    with get_connection() as conn:
        conn.execute("TRUNCATE TABLE links")
    yield
