from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Request, Depends

from sqlalchemy import func
from sqlmodel import Session, select

from timescaledb.hyperfunctions import time_bucket
from timescaledb.utils import get_utc_now

from api.db.session import get_session
from api.watch_sessions.models import WatchSession

from .models import YouTubePlayerState, YouTubeWatchEvent, YouTubeWatchEventResponseModel

router = APIRouter()

@router.post("/", response_model=YouTubeWatchEventResponseModel) # /api/video-events/
def create_video_event(
        request: Request, 
        payload: YouTubePlayerState,
        db_session: Session = Depends(get_session)  
    ):
    headers = request.headers
    watch_session_id = headers.get('x-session-id')
    print('session id', watch_session_id)
    print()
    referer = headers.get("referer")
    # print(db_session)
    data = payload.model_dump()
    # data["referer"] = referer
    obj = YouTubeWatchEvent(**data)
    obj.referer = referer
    if watch_session_id:
        watch_session_query = select(WatchSession).where(WatchSession.watch_session_id==watch_session_id)
        watch_session_obj = db_session.exec(watch_session_query).first()
        if watch_session_obj:
            obj.watch_session_id = watch_session_id
            watch_session_obj.last_active = get_utc_now()
            db_session.add(watch_session_obj)
    db_session.add(obj)
    db_session.commit()
    db_session.refresh(obj)
    print(obj)
    # print(data, referer)
    return obj


@router.get("/{video_id}")
def get_video_stats(
        video_id:str,
        db_session: Session = Depends(get_session)  
    ):
    bucket = time_bucket("1 minute", YouTubeWatchEvent.time)
    start = datetime.now(timezone.utc) - timedelta(hours=25)
    end = datetime.now(timezone.utc) - timedelta(hours=1)
    query = (
        select(
            bucket, # 0
            YouTubeWatchEvent.video_id, # 1
            func.count().label("total_events") # 2
        )
        .where(
            YouTubeWatchEvent.time > start,
            YouTubeWatchEvent.time <= end,
            YouTubeWatchEvent.video_id == video_id
        )
        .group_by(
            bucket,
            YouTubeWatchEvent.video_id
        )
        .order_by(
            bucket,
            YouTubeWatchEvent.video_id
        )

    )
    results = db_session.exec(query).fetchall()
    results = [(str(x[0]), str(x[1]), str(x[2]) ) for x in results]
    print(results)
    return results