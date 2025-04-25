from typing import List
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Request, Depends, HTTPException

from sqlalchemy import func
from sqlmodel import Session, select

from timescaledb.hyperfunctions import time_bucket
from timescaledb.utils import get_utc_now

from api.utils import parse_int_or_fallback
from api.db.session import get_session
from api.watch_sessions.models import WatchSession

from .models import (
    YouTubePlayerState, 
    YouTubeWatchEvent, 
    YouTubeWatchEventResponseModel,
    VideoStat
)

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




@router.get("/top", response_model=List[VideoStat])
def get_top_video_stats(
        request: Request,
        db_session: Session = Depends(get_session)  
    ):
    params = request.query_params
    bucket_param = params.get("bucket") or "1 day"
    bucket = time_bucket(bucket_param, YouTubeWatchEvent.time)
    hours_ago = parse_int_or_fallback(params.get("hours-ago"), fallback=10)
    hours_until = parse_int_or_fallback(params.get("hours-until"), fallback=0)
    start = datetime.now(timezone.utc) - timedelta(hours=hours_ago)
    end = datetime.now(timezone.utc) - timedelta(hours=hours_until)
    unique_views = func.count(func.distinct(YouTubeWatchEvent.watch_session_id)).label("unique_views")
    query = (
        select(
            bucket, # 0
            YouTubeWatchEvent.video_id, # 1
            func.count().label("total_events"), # 2
            func.max(YouTubeWatchEvent.current_time).label("max_viewership"), # in seconds
            func.avg(YouTubeWatchEvent.current_time).label("avg_viewership"), # in seconds
            unique_views
        )
        .where(
            YouTubeWatchEvent.time > start,
            YouTubeWatchEvent.time <= end,
            YouTubeWatchEvent.video_state_label != "CUED",
        )
        .group_by(
            bucket,
            YouTubeWatchEvent.video_id
        )
        .order_by(
            bucket.desc(),
            unique_views.desc(),
            YouTubeWatchEvent.video_id
        )

    )
    try:
        results = db_session.exec(query).fetchall()
    except:
        raise HTTPException(
            status_code=400,
            detail='Invalid query'
        )
    results = [
        VideoStat(
        time=x[0],
        video_id=x[1],
        total_events=x[2],
        max_viewership=x[3],
        avg_viewership=x[4],
        unique_views=x[5],
    ) for x in results]
    return results



@router.get("/{video_id}", response_model=List[VideoStat])
def get_video_stats(
        video_id:str,
        request: Request,
        db_session: Session = Depends(get_session)  
    ):
    params = request.query_params
    bucket_param = params.get("bucket") or "1 day"
    bucket = time_bucket(bucket_param, YouTubeWatchEvent.time)
    hours_ago = parse_int_or_fallback(params.get("hours-ago"), fallback=24 * 31 * 3)
    hours_until = parse_int_or_fallback(params.get("hours-until"), fallback=0)
    start = datetime.now(timezone.utc) - timedelta(hours=hours_ago)
    end = datetime.now(timezone.utc) - timedelta(hours=hours_until)
    query = (
        select(
            bucket, # 0
            YouTubeWatchEvent.video_id, # 1
            func.count().label("total_events"), # 2
            func.max(YouTubeWatchEvent.current_time).label("max_viewership"), # in seconds
            func.avg(YouTubeWatchEvent.current_time).label("avg_viewership"), # in seconds
            func.count(func.distinct(YouTubeWatchEvent.watch_session_id)).label("unique_views")
        )
        .where(
            YouTubeWatchEvent.time > start,
            YouTubeWatchEvent.time <= end,
            YouTubeWatchEvent.video_state_label != "CUED",
            YouTubeWatchEvent.video_id == video_id
        )
        .group_by(
            bucket,
            YouTubeWatchEvent.video_id
        )
        .order_by(
            bucket.desc(),
            YouTubeWatchEvent.video_id
        )

    )
    try:
        results = db_session.exec(query).fetchall()
    except:
        raise HTTPException(
            status_code=400,
            detail='Invalid query'
        )
    results = [
        VideoStat(
        time=x[0],
        video_id=x[1],
        total_events=x[2],
        max_viewership=x[3],
        avg_viewership=x[4],
        unique_views=x[5],
    ) for x in results]
    return results