from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.services.video_service import VideoService
from app.schemas.video import ProcessRequest, VideoInfo
from app.db.connection import get_video_service

router = APIRouter()

@router.post("/process", response_model=List[VideoInfo])
async def process_videos(
    process_request: ProcessRequest,
    video_service: VideoService = Depends(get_video_service)
):
    try:
        processed_videos = await video_service.process_tasks(process_request.task_ids)
        return processed_videos
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))