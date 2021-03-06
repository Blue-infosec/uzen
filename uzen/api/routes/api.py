from fastapi import APIRouter

from uzen.api.routes import snapshots, urlscan, yara, scripts

api_router = APIRouter()
api_router.include_router(snapshots.router, prefix="/snapshots", tags=["Snapshots"])
api_router.include_router(urlscan.router, prefix="/import", tags=["Import"])
api_router.include_router(yara.router, prefix="/yara", tags=["YARA"])
api_router.include_router(scripts.router, prefix="/scripts", tags=["Scripts"])
