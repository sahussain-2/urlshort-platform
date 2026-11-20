import secrets

from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

app = FastAPI(title="urlshort-platform")

links: dict[str, str] = {}

class LinkCreate(BaseModel):
    url: str


@app.get("/health")
def health():
    return {"status": "ok", "service": "urlshort"}


@app.post("/links")
def create_link(payload: LinkCreate):
    code = secrets.token_urlsafe(5)
    links[code] = payload.url
    return {"code": code, "url": payload.url}

@app.get("/{code}")
def follow_link(code: str):
    url = links.get(code)
    if url is None:
        raise HTTPException(status_code=404, detail="Link not found")
    return RedirectResponse(url=url)
