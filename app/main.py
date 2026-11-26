import logging
import secrets

from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from psycopg.errors import UniqueViolation
from pydantic import BaseModel, HttpUrl

from app import storage
from app.config import BASE_URL, LOG_LEVEL

app = FastAPI(title="urlshort-platform")
logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
logger = logging.getLogger("urlshort")


class LinkCreate(BaseModel):
    url: HttpUrl


@app.get("/health")
def health():
    return {"status": "ok", "service": "urlshort"}


@app.post("/links")
def create_link(payload: LinkCreate):
    url = str(payload.url)
    for _ in range(5):
        code = secrets.token_urlsafe(5)
        try:
            storage.create_link(code, url)
        except UniqueViolation:
            logger.warning("code collision code=%s", code)
            continue
        logger.info("link created code=%s", code)
        return {
            "code": code,
            "url": url,
            "short_url": f"{BASE_URL}/{code}",
        }
    raise HTTPException(status_code=500, detail="Could not generate a unique code")


@app.get("/links/{code}/stats")
def link_stats(code: str):
    row = storage.get_stats(code)
    if row is None:
        logger.warning("unknown code=%s", code)
        raise HTTPException(status_code=404, detail="Link not found")
    url, clicks_count = row
    return {"code": code, "url": url, "clicks": clicks_count}


@app.get("/{code}")
def follow_link(code: str):
    url = storage.get_url(code)
    if url is None:
        logger.warning("unknown code=%s", code)
        raise HTTPException(status_code=404, detail="Link not found")
    clicks = storage.increment_clicks(code)
    logger.info("redirect code=%s clicks=%d", code, clicks)
    return RedirectResponse(url=url)
