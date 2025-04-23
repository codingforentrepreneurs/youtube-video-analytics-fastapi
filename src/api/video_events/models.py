from typing import Optional

from sqlmodel import SQLModel, Field


class YouTubeWatchEvent(SQLModel, table=True):
    id: int = Field(primary_key=True)
    is_ready: bool 
    video_id: str = Field(index=True)
    video_title: str
    current_time: float
    video_state_label: str
    video_state_value: int
    referer: Optional[str] = Field(default="", index=True)


class YouTubePlayerState(SQLModel, table=False):
    is_ready: bool 
    video_id: str = Field(index=True)
    video_title: str
    current_time: float
    video_state_label: str
    video_state_value: int


class YouTubeWatchEventResponseModel(SQLModel, table=False):
    id: int = Field(primary_key=True)
    video_id: str = Field(index=True)
    current_time: float