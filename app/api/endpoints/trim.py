from fastapi import APIRouter, HTTPException, Depends
from app.services.video_service import VideoService
from app.schemas.video import TrimRequest, VideoInfo
from app.db.connection import get_video_service

router = APIRouter()

@router.post("/trim", response_model=int)
async def trim_video(
    trim_request: TrimRequest,
    video_service: VideoService = Depends(get_video_service)
):
    try:
        task_id = await video_service.add_trim_task(
            trim_request.video_id,
            trim_request.start_time,
            trim_request.end_time
        )
        return task_id
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))