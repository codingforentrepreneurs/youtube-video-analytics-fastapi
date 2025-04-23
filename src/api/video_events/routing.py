from fastapi import APIRouter, Request

from .models import YouTubePlayerState

router = APIRouter()

@router.post("/") # /api/video-events/
def create_video_event(request: Request, payload: YouTubePlayerState):
    headers = request.headers
    referer = headers.get("referer")
    data = payload.model_dump()
    print(data, referer)
    return data