import secrets

from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

app = FastAPI(title="urlshort-platform")

links: dict[str, str] = {}
clicks: dict[str, int] = {}

class LinkCreate(BaseModel):
    url: str


@app.get("/health")
def health():
    return {"status": "ok", "service": "urlshort"}


@app.post("/links")
def create_link(payload: LinkCreate):
    code = secrets.token_urlsafe(5)
    links[code] = payload.url
    clicks[code] = 0
    return {"code": code, "url": payload.url}

@app.get("/links/{code}/stats")
def link_stats(code: str):
    if code not in links:
        raise HTTPException(status_code=404, detail="Link not found")
    return {"code": code, "url": links[code], "clicks": clicks[code]}

@app.get("/{code}")
def follow_link(code: str):
    url = links.get(code)
    if url is None:
        raise HTTPException(status_code=404, detail="Link not found")
    clicks[code] += 1
    return RedirectResponse(url=url)
