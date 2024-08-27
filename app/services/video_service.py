import uuid
from fastapi import UploadFile
from sqlalchemy.orm import Session
from app.models.video import Video
from app.models.video_task import VideoTask, TaskStatus
from app.schemas.video import VideoInfo, DetailedVideoInfo, AllVideosInfo, VideoTaskInfo, VideoType, VideoTaskType, VideoTaskStatus
from app.services.ffmpeg_service import FFmpegService
from app.core.errors import handle_video_not_found, handle_video_processing_error
from typing import List

class VideoService:
    def __init__(self, db: Session):
        self.db = db
        self.ffmpeg_service = FFmpegService()


    async def save_video(self, file: UploadFile) -> VideoInfo:
        video_id = str(uuid.uuid4())
        file_path = f"static/videos/{video_id}.mp4"

        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())
        
        video_info = self.ffmpeg_service.get_video_info(file_path)
        
        video = Video(id=video_id, filename=file.filename, file_path=file_path, **video_info)
        self.db.add(video)
        self.db.commit()
        
        return VideoInfo.model_validate(video)


    async def get_video_info(self, video_id: str) -> VideoInfo:
        video = self.db.query(Video).filter(Video.id == video_id).first()
        if not video:
            handle_video_not_found(video_id)
        return VideoInfo.model_validate(video)


    async def get_all_videos_info(self) -> List[VideoInfo]:
        videos = self.db.query(Video).all()
        return [VideoInfo.model_validate(video) for video in videos]
    

    async def get_all_videos_and_tasks_info(self) -> AllVideosInfo:
        videos = self.db.query(Video).all()
        tasks = self.db.query(VideoTask).all()

        detailed_videos = []
        for video in videos:
            related_tasks = [
                VideoTaskInfo(
                    id=task.id,
                    task_type=VideoTaskType(task.task_type),
                    status=VideoTaskStatus(task.status.value),
                    video_ids=task.video_ids,
                    parameters=task.parameters,
                    result_video_id=task.result_video_id
                )
                for task in tasks if video.id in task.video_ids or task.result_video_id == video.id
            ]

            detailed_videos.append(
                DetailedVideoInfo(
                    id=video.id,
                    filename=video.filename,
                    file_url=f"/static/videos/{video.id}.mp4",
                    video_type=VideoType.ORIGINAL if not video.id.startswith("trim_") and not video.id.startswith("concat_") else (VideoType.TRIMMED if video.id.startswith("trim_") else VideoType.CONCATENATED),
                    duration=video.duration,
                    format=video.format,
                    width=video.width,
                    height=video.height,
                    related_tasks=related_tasks
                )
            )

        all_tasks = [
            VideoTaskInfo(
                id=task.id,
                task_type=VideoTaskType(task.task_type),
                status=VideoTaskStatus(task.status.value),
                video_ids=task.video_ids,
                parameters=task.parameters,
                result_video_id=task.result_video_id
            )
            for task in tasks
        ]

        return AllVideosInfo(videos=detailed_videos, tasks=all_tasks)


    async def trim_video(self, video_id: str, start_time: float, end_time: float) -> VideoInfo:
        video = self.db.query(Video).filter(Video.id == video_id).first()
        if not video:
            handle_video_not_found(video_id)
        
        output_path = f"static/videos/{video_id}_trimmed.mp4"
        
        try:
            self.ffmpeg_service.trim_video(video.file_path, output_path, start_time, end_time)
        except Exception as e:
            handle_video_processing_error(str(e))
        
        video_info = self.ffmpeg_service.get_video_info(output_path)
        
        trimmed_video = Video(id=str(uuid.uuid4()), filename=f"{video.filename}_trimmed", file_path=output_path, **video_info)
        self.db.add(trimmed_video)
        self.db.commit()

        return VideoInfo.model_validate(trimmed_video)


    async def concat_videos(self, video_ids: list[str]) -> VideoInfo:
        videos = self.db.query(Video).filter(Video.id.in_(video_ids)).all()
        if len(videos) != len(video_ids):
            handle_video_not_found("One or more videos not found")
        
        output_path = f"static/videos/concatenated_{uuid.uuid4()}.mp4"
        try:
            self.ffmpeg_service.concat_videos([video.file_path for video in videos], output_path)
        except Exception as e:
            handle_video_processing_error(str(e))
        
        video_info = self.ffmpeg_service.get_video_info(output_path)
        
        concat_video = Video(id=str(uuid.uuid4()), filename="concatenated_video", file_path=output_path, **video_info)
        self.db.add(concat_video)
        self.db.commit()
        
        return VideoInfo.model_validate(concat_video)


    async def get_video_path(self, video_id: str) -> str:
        video = self.db.query(Video).filter(Video.id == video_id).first()
        if not video:
            handle_video_not_found(video_id)
        return video.file_path
    

    async def add_trim_task(self, video_id: str, start_time: float, end_time: float) -> int:
        task = VideoTask(
            task_type="trim",
            video_ids=[video_id],
            parameters={"start_time": start_time, "end_time": end_time}
        )
        self.db.add(task)
        self.db.commit()
        return task.id

    async def add_concat_task(self, video_ids: list[str]) -> int:
        task = VideoTask(
            task_type="concat",
            video_ids=video_ids,
            parameters={}
        )
        self.db.add(task)
        self.db.commit()
        return task.id

    async def process_tasks(self, task_ids: list[int]) -> list[VideoInfo]:
        results = []
        for task_id in task_ids:
            task = self.db.query(VideoTask).filter(VideoTask.id == task_id).first()
            if not task:
                continue

            task.status = TaskStatus.PROCESSING
            self.db.commit()

            try:
                if task.task_type == "trim":
                    video_info = await self.trim_video(task.video_ids[0], task.parameters['start_time'], task.parameters['end_time'])
                elif task.task_type == "concat":
                    video_info = await self.concat_videos(task.video_ids)
                
                task.status = TaskStatus.COMPLETED
                task.result_video_id = video_info.id
                results.append(video_info)
            except Exception as e:
                task.status = TaskStatus.FAILED
                pass

            self.db.commit()

        return results