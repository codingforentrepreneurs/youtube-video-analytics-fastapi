from contextlib import asynccontextmanager
from typing import Union

from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):
    # before app startup up
    # init_db()
    yield
    # clean up


app = FastAPI(lifespan=lifespan)
# app.include_router(event_router, prefix='/api/events')
# /api/events


@app.get("/")
def read_root():
    return {"Hello": "World my old friend"}


@app.get("/healthz")
def read_api_health():
    return {"status": "ok"}