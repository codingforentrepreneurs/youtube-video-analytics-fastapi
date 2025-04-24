from datetime import datetime
from typing import Optional

from timescaledb import TimescaleModel
from pydantic import BaseModel, Field as PydanticField
from sqlmodel import SQLModel, Field


class YouTubeWatchEvent(TimescaleModel, table=True):
    # id: int = Field(primary_key=True)
    is_ready: bool 
    video_id: str = Field(index=True)
    video_title: str
    current_time: float
    video_state_label: str
    video_state_value: int
    referer: Optional[str] = Field(default="", index=True)
    watch_session_id: Optional[str] = Field(index=True)

    # timescaledb config
    __chunk_time_interval__ = "INTERVAL 7 days"
    __drop_after__ = "INTERVAL 1 year"
    __enable_compression__ = True
    __compress_orderby__ = "time DESC"
    __compress_segmentby__ = "video_id"  
    __migrate_data__ = True
    __if_not_exists__ = True


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
    time: datetime



class VideoStat(BaseModel):
    time: datetime
    video_id: str
    total_events: int
    max_viewership: Optional[float] = PydanticField(default=-1)
    avg_viewership: Optional[float] = PydanticField(default=-1)
    unique_views: Optional[int] = PydanticField(default=-1)