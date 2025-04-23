from typing import Optional

from sqlmodel import SQLModel, Field


class YouTubeWatchEvent(SQLModel, table=False):
    id: int = Field(primary_key=True)
    is_ready: bool 
    video_id: str = Field(index=True)
    video_title: str
    current_time: float
    video_state_label: str
    video_state_value: int

class YouTubePlayerState(SQLModel, table=False):
    is_ready: bool 
    video_id: str = Field(index=True)
    video_title: str
    current_time: float
    video_state_label: str
    video_state_value: int