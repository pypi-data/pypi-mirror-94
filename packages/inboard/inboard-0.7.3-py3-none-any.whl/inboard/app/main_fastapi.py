import os
import sys
from typing import Dict

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from inboard.app.utilities_fastapi import Settings, basic_auth

origin_regex = r"^(https?:\/\/)(localhost|([\w\.]+\.)?br3ndon.land)(:[0-9]+)?$"
server = "Uvicorn" if bool(os.getenv("WITH_RELOAD")) else "Uvicorn, Gunicorn"
version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"

settings = Settings()

app = FastAPI(title=settings.name, version=settings.version)
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_headers=["*"],
    allow_methods=["*"],
    allow_origin_regex=origin_regex,
)


@app.get("/")
async def get_root() -> Dict[str, str]:
    return {"Hello": "World"}


@app.get("/health")
async def get_health(auth: str = Depends(basic_auth)) -> Dict[str, str]:
    return {"application": app.title, "status": "active"}


@app.get("/status")
async def get_status(auth: str = Depends(basic_auth)) -> Dict[str, str]:
    message = f"Hello World, from {server}, FastAPI, and Python {version}!"
    return {"application": app.title, "status": "active", "message": message}


@app.get("/users/me")
async def get_current_user(username: str = Depends(basic_auth)) -> Dict[str, str]:
    return {"username": username}
