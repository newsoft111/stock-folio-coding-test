from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import FileResponse
from app.services.video_service import VideoService
from app.db.connection import get_video_service

router = APIRouter()

@router.get("/download/{video_id}")
async def download_video(
    video_id: str,
    video_service: VideoService = Depends(get_video_service)
):
    try:
        video_path = await video_service.get_video_path(video_id)
        return FileResponse(video_path, media_type="video/mp4", filename=f"{video_id}.mp4")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))