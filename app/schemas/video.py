from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from enum import Enum

class VideoType(str, Enum):
    ORIGINAL = "original"
    TRIMMED = "trimmed"
    CONCATENATED = "concatenated"

class VideoTaskType(str, Enum):
    TRIM = "trim"
    CONCAT = "concat"

class VideoTaskStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class VideoTaskInfo(BaseModel):
    id: int
    task_type: VideoTaskType
    status: VideoTaskStatus
    video_ids: List[str]
    parameters: dict
    result_video_id: Optional[str]

class DetailedVideoInfo(BaseModel):
    id: str
    filename: str
    file_url: str
    video_type: VideoType
    duration: float
    format: str
    width: int
    height: int
    related_tasks: List[VideoTaskInfo]

class AllVideosInfo(BaseModel):
    videos: List[DetailedVideoInfo]
    tasks: List[VideoTaskInfo]

class VideoBase(BaseModel):
    filename: str
    duration: float
    format: str
    width: int
    height: int

class VideoCreate(VideoBase):
    pass

class VideoInfo(VideoBase):
    id: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class TrimRequest(BaseModel):
    video_id: str
    start_time: float
    end_time: float

class ConcatRequest(BaseModel):
    video_ids: List[str]

class ProcessRequest(BaseModel):
    task_ids: List[int]

class VideoList(BaseModel):
    videos: List[VideoInfo]