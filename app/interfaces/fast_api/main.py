# flake8: noqa
# ruff: noqa
# mypy: ignore-errors
import logging
import sys
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from core.config.settings import settings
from core.enums.di.storage import StorageType
from core.i18n import activate as activate_language, reset as reset_language
from core.init_services import init_services, shutdown_services
from interfaces.fast_api.routers import auth_router

load_dotenv()
from fastadmin import fastapi_app as admin_app

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)

app = FastAPI()
allowed_origins = settings.system.get_allowed_origins()

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def localization_middleware(request: Request, call_next):
    language = activate_language(
        language=request.query_params.get("lang"),
        accept_language=request.headers.get("Accept-Language"),
    )
    request.state.language = language
    try:
        response = await call_next(request)
    finally:
        reset_language()
    response.headers["Content-Language"] = request.state.language
    return response


LOCAL_FILES_ROUTE = f"/{settings.storage.local_base_url.strip('/')}" + "/{file_path:path}"


@app.get(LOCAL_FILES_ROUTE)
async def get_upload_file(file_path: str) -> FileResponse:
    if settings.storage.type != StorageType.LOCAL:
        raise HTTPException(status_code=404, detail="File not found")

    root = settings.storage.get_local_upload_dir().resolve()
    full_path = (root / file_path).resolve()
    try:
        full_path.relative_to(root)
    except ValueError:
        raise HTTPException(status_code=404, detail="File not found")
    if not full_path.is_file():
        raise HTTPException(status_code=404, detail="File not found")

    response = FileResponse(Path(full_path))
    if allowed_origins == ["*"]:
        response.headers["Access-Control-Allow-Origin"] = "*"
    else:
        response.headers["Access-Control-Allow-Origin"] = ",".join(allowed_origins)
    response.headers["Access-Control-Allow-Credentials"] = "true"
    return response


async def startup() -> None:
    await init_services()


async def shutdown() -> None:
    await shutdown_services()


app.add_event_handler("startup", startup)
app.add_event_handler("shutdown", shutdown)

app.include_router(auth_router, prefix=settings.system.api_v1)
app.mount("/admin", admin_app, name="admin")
