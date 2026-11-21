import logging
import secrets

from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, HttpUrl

from app.config import BASE_URL, LOG_LEVEL

app = FastAPI(title="urlshort-platform")
logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
logger = logging.getLogger("urlshort")
links: dict[str, str] = {}
clicks: dict[str, int] = {}


class LinkCreate(BaseModel):
    url: HttpUrl


@app.get("/health")
def health():
    return {"status": "ok", "service": "urlshort"}


@app.post("/links")
def create_link(payload: LinkCreate):
    code = secrets.token_urlsafe(5)
    url = str(payload.url)
    links[code] = url
    clicks[code] = 0
    logger.info("link created code=%s", code)
    return {
        "code": code,
        "url": url,
        "short_url": f"{BASE_URL}/{code}",
    }


@app.get("/links/{code}/stats")
def link_stats(code: str):
    if code not in links:
        logger.warning("unknown code=%s", code)
        raise HTTPException(status_code=404, detail="Link not found")
    return {"code": code, "url": links[code], "clicks": clicks[code]}


@app.get("/{code}")
def follow_link(code: str):
    url = links.get(code)
    if url is None:
        logger.warning("unknown code=%s", code)
        raise HTTPException(status_code=404, detail="Link not found")
    clicks[code] += 1
    logger.info("redirect code=%s clicks=%d", code, clicks[code])
    return RedirectResponse(url=url)
