from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.services.video_service import VideoService
from app.schemas.video import VideoInfo, AllVideosInfo
from app.db.connection import get_video_service

router = APIRouter()

@router.get("/info/{video_id}", response_model=VideoInfo)
async def get_video_info(
    video_id: str,
    video_service: VideoService = Depends(get_video_service)
):
    try:
        video_info = await video_service.get_video_info(video_id)
        if not video_info:
            raise HTTPException(status_code=404, detail="Video not found")
        return video_info
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/info", response_model=List[VideoInfo])
async def get_all_videos_info(
    video_service: VideoService = Depends(get_video_service)
):
    try:
        all_videos_info = await video_service.get_all_videos_info()
        return all_videos_info
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    


@router.get("/all_info", response_model=AllVideosInfo)
async def get_all_videos_and_tasks_info(
    video_service: VideoService = Depends(get_video_service)
):
    try:
        all_info = await video_service.get_all_videos_and_tasks_info()
        return all_info
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))