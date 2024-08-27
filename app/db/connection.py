from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.services.video_service import VideoService
from fastapi import Depends

def get_db():
	db = SessionLocal()
	try:
		yield db # DB 연결 성공한 경우, DB 세션 시작
	finally:
		db.close()
		# db 세션이 시작된 후, API 호출이 마무리되면 DB 세션을 닫아준다.


def get_video_service(db: Session = Depends(get_db)):
    return VideoService(db)