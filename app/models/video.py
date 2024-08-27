from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from app.db.session import Base



class Video(Base):
    __tablename__ = "videos"

    id = Column(String, primary_key=True, index=True)
    filename = Column(String, index=True)
    file_path = Column(String)
    duration = Column(Float)
    format = Column(String)
    width = Column(Integer)
    height = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())