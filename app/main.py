from fastapi import FastAPI

app = FastAPI(title="urlshort-platform")


@app.get("/health")
def health():
    return {"status": "ok", "service": "urlshorts"}