from sqlalchemy import Column, Integer, String, JSON, DateTime, Enum
from sqlalchemy.sql import func
from app.db.session import Base
import enum

class TaskStatus(enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class VideoTask(Base):
    __tablename__ = "video_tasks"

    id = Column(Integer, primary_key=True, index=True)
    task_type = Column(String)  # 'trim' 또는 'concat'
    video_ids = Column(JSON)  # trim의 경우 단일 ID, concat의 경우 여러 ID
    parameters = Column(JSON)  # trim의 경우 start_time과 end_time, concat의 경우 빈 딕셔너리
    status = Column(Enum(TaskStatus), default=TaskStatus.PENDING)
    result_video_id = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())