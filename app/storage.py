import psycopg

from app.config import DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER


def get_connection():

    return psycopg.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
    )


def get_url(code):

    with get_connection() as conn:
        row = conn.execute("SELECT url FROM links WHERE code = %s", (code,)).fetchone()
    if row is None:
        return None
    return row[0]


def create_link(code, url):

    with get_connection() as conn:
        conn.execute(
            "INSERT INTO links (code, url) VALUES (%s, %s)",
            (code, url),
        )


def increment_clicks(code):

    with get_connection() as conn:
        row = conn.execute(
            "UPDATE links SET clicks = clicks + 1 WHERE code = %s RETURNING clicks",
            (code,),
        ).fetchone()
    if row is None:
        return None
    return row[0]


def get_stats(code):

    with get_connection() as conn:
        row = conn.execute(
            "SELECT url, clicks FROM links WHERE code = %s",
            (code,),
        ).fetchone()
    return row


def init_db():

    with get_connection() as conn:
        conn.execute(
            "CREATE TABLE IF NOT EXISTS links ("
            "code text PRIMARY KEY, "
            "url text NOT NULL, "
            "clicks integer NOT NULL DEFAULT 0)"
        )
