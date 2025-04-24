from fastapi import APIRouter, Request, Depends

from sqlmodel import Session

from api.db.session import get_session

from .models import YouTubePlayerState, YouTubeWatchEvent, YouTubeWatchEventResponseModel

router = APIRouter()

@router.post("/", response_model=YouTubeWatchEventResponseModel) # /api/video-events/
def create_video_event(
        request: Request, 
        payload: YouTubePlayerState,
        db_session: Session = Depends(get_session)  
    ):
    headers = request.headers
    session_id = headers.get('x-session-id')
    print('session id', session_id)
    print()
    referer = headers.get("referer")
    # print(db_session)
    data = payload.model_dump()
    # data["referer"] = referer
    obj = YouTubeWatchEvent(**data)
    obj.referer = referer
    obj.watch_session_id = session_id
    db_session.add(obj)
    db_session.commit()
    db_session.refresh(obj)
    print(obj)
    # print(data, referer)
    return obj