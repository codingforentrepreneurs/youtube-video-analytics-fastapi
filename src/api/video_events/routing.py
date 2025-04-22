from pydantic import BaseModel
from fastapi import APIRouter

router = APIRouter()

class YoutubeVideoData(BaseModel):
    title: str

class YouTubePlayerState(BaseModel):
    isReady: bool
    videoData: YoutubeVideoData
    currentTime: int
    videoStateLabel: str
    videoStateValue: int

@router.post("/") # /api/video-events/
def create_video_event(payload: YouTubePlayerState):
    data = payload.model_dump()
    print(data)
    return data