from fastapi import HTTPException, status

class VideoNotFoundError(HTTPException):
    def __init__(self, video_id: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Video with id {video_id} not found"
        )

class VideoProcessingError(HTTPException):
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing video: {detail}"
        )

class InvalidVideoFormatError(HTTPException):
    def __init__(self, format: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid video format: {format}"
        )

class UnauthorizedError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

class ForbiddenError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )

def handle_video_not_found(video_id: str):
    raise VideoNotFoundError(video_id)

def handle_video_processing_error(detail: str):
    raise VideoProcessingError(detail)

def handle_invalid_video_format(format: str):
    raise InvalidVideoFormatError(format)

def handle_unauthorized():
    raise UnauthorizedError()

def handle_forbidden():
    raise ForbiddenError()