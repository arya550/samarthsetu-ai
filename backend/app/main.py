"""
SamarthSetu AI — FastAPI application entry point.

Serves both the JSON API (/api/*) and the no-build frontend (static files),
so the whole prototype runs with a single command:

    uvicorn app.main:app --port 8000
"""
from __future__ import annotations

import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.api import core, health, profile

app = FastAPI(
    title="SamarthSetu AI API",
    description="AI-assisted scheme matching and access pathway prototype — "
                "From Eligibility to Access.",
    version="1.0.0",
)

# CORS: permissive origins allowed because this is a localhost prototype;
# tighten via ALLOWED_ORIGINS env var when deploying.
allowed_origins = os.getenv("ALLOWED_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in allowed_origins],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API routers
app.include_router(health.router, prefix="/api", tags=["health"])
app.include_router(profile.router, prefix="/api", tags=["profile"])
app.include_router(core.router, prefix="/api", tags=["core"])


@app.get("/")
async def root():
    return {
        "name": "SamarthSetu AI",
        "tagline": "From Eligibility to Access",
        "message": "API running. Open /app for the UI, /docs for API docs.",
        "app_url": "/app/",
        "docs_url": "/docs",
    }


# ---------------------------------------------------------------------------
# No-build frontend (served by the backend so localhost testing needs nothing
# but Python). Static assets under /static, SPA entry at /app.
# ---------------------------------------------------------------------------
FRONTEND_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "frontend",
)
STATIC_DIR = os.path.join(FRONTEND_DIR, "static")
INDEX_FILE = os.path.join(FRONTEND_DIR, "index.html")

if os.path.isdir(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/app")
@app.get("/app/{rest:path}")
async def serve_app(rest: str = ""):
    if os.path.isfile(INDEX_FILE):
        return FileResponse(INDEX_FILE)
    return {"error": "Frontend not built. See README for setup."}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", "8000")))
