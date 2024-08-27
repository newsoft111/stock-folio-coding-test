from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.services.video_service import VideoService
from app.schemas.video import ConcatRequest, VideoInfo
from app.db.connection import get_video_service

router = APIRouter()

@router.post("/concat", response_model=int)
async def concat_videos(
    concat_request: ConcatRequest,
    video_service: VideoService = Depends(get_video_service)
):
    try:
        task_id = await video_service.add_concat_task(concat_request.video_ids)
        return task_id
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))