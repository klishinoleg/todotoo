# flake8: noqa
# ruff: noqa
# mypy: ignore-errors
import asyncio
import logging
import os
import sys

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi18n.middlewares import LocalizationMiddleware
from fastapi.middleware.cors import CORSMiddleware

from core.init_services import init_services, shutdown_services
from interfaces.fast_api.routers import auth_router
from core.config.settings import settings
from fastapi import HTTPException
from fastapi.responses import FileResponse
import core.i18n

load_dotenv()
from fastadmin import fastapi_app as admin_app

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.system.get_allow_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(LocalizationMiddleware)


@app.get("/" + settings.system.images_upload_url + "/{file_path:path}")
async def get_upload_file(file_path: str) -> FileResponse:
    full_path = os.path.join(settings.get_upload_dir(), file_path)
    if not os.path.isfile(full_path):
        raise HTTPException(status_code=404, detail="File not found")

    response = FileResponse(full_path)
    response.headers["Access-Control-Allow-Origin"] = ",".join(settings.get_allow_origins())
    response.headers["Access-Control-Allow-Credentials"] = "true"
    return response


async def startup() -> None:
    await init_services()


async def shutdown() -> None:
    await shutdown_services()


app.add_event_handler("startup", startup)
app.add_event_handler("shutdown", shutdown)

app.include_router(auth_router, prefix=settings.api_v1)
app.mount("/admin", admin_app, name="admin")

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
