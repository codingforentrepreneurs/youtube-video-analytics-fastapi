import uuid
from datetime import datetime
from typing import Optional

from timescaledb import TimescaleModel
from timescaledb.utils import get_utc_now
from sqlmodel import SQLModel, Field

def generate_session_id():
    return str(uuid.uuid4())


class WatchSession(TimescaleModel, table=True):
    # id: int = Field(primary_key=True)
    watch_session_id: str = Field(default_factory=generate_session_id, index=True)
    path: Optional[str]  = Field(default="", index=True)
    referer: Optional[str] = Field(default="", index=True)
    video_id: Optional[str] = Field(default="", index=True)
    last_active: Optional[datetime] = Field(default_factory=get_utc_now)

    # timescaledb config
    __chunk_time_interval__ = "INTERVAL 30 days"
    __drop_after__ = "INTERVAL 3 years"



class WatchSessionCreate(SQLModel, table=False):
    path: Optional[str] = Field(default="")
    video_id: Optional[str] = Field(default="", index=True)