from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import JSONResponse
from app.db.connection import get_video_service
from typing import List
from app.services.video_service import VideoService
from app.schemas.video import VideoInfo
from app.core.config import upload_settings
import os

router = APIRouter()

@router.post("/upload", response_model=VideoInfo)
async def upload_video(
    file: UploadFile = File(...),
    video_service: VideoService = Depends(get_video_service)
):
    # 파일 확장자 검사
    allowed_extensions = [".mp4", ".avi", ".mov"]
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in allowed_extensions:
        raise HTTPException(status_code=400, detail="Unsupported file format")

    # 파일 크기 검사
    if file.size > upload_settings.MAX_UPLOAD_SIZE:
        raise HTTPException(status_code=400, detail="File too large")

    try:
        # 파일 저장 및 메타데이터 추출
        video_info = await video_service.save_video(file)
        return video_info
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
