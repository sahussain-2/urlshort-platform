# urlshort-platform

A URL shortener service, built as a hands-on project to learn DevOps tools.

## Goal

Use the service as a realistic base to practice Docker, Ansible, Python, GitHub and Terraform.

## Features

- Create a short link: `POST /links`
- Redirect: `GET /{code}`
- Click statistics: `GET /links/{code}/stats`
- Health check: `GET /health`

## Quick start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
uvicorn app.main:app
```

Interactive docs: http://127.0.0.1:8000/docs

## Configuration

Settings come from environment variables. See `.env.example`.

| Variable | Default | Purpose |
|---|---|---|
| `BASE_URL` | `http://127.0.0.1:8000` | Base of the returned short URL |
| `LOG_LEVEL` | `INFO` | Logging verbosity |

## Make targets

Run `make help` to list them: `lint`, `format`, `test`, `check`.

## Status

Phase 1 (application, tests, lint) is done.
