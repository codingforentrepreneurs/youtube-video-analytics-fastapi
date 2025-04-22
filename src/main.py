from contextlib import asynccontextmanager
from typing import Union

from fastapi import FastAPI

from api.video_events.routing import router as video_events_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # before app startup up
    # init_db()
    yield
    # clean up


app = FastAPI(lifespan=lifespan)
app.include_router(video_events_router, prefix='/api/video-events')
# /api/events


@app.get("/")
def read_root():
    return {"Hello": "World my old friend"}


@app.get("/healthz")
def read_api_health():
    return {"status": "ok"}