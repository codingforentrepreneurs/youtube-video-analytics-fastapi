from typing import Optional
from pydantic import BaseModel, Field
from fastapi import APIRouter, Request

router = APIRouter()

class YouTubePlayerState(BaseModel):
    is_ready: bool
    video_id: str
    video_title: str
    current_time: float
    video_state_label: str
    video_state_value: int

@router.post("/") # /api/video-events/
def create_video_event(request: Request, payload: YouTubePlayerState):
    headers = request.headers
    referer = headers.get("referer")
    data = payload.model_dump()
    print(data, referer)
    return data