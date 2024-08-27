#poetry run uvicorn main:app --reload --host=0.0.0.0 --port=8000
from fastapi import FastAPI, Depends, Path, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from app.core.config import media_settings
from fastapi.middleware.cors import CORSMiddleware
import app.models as models
from app.api.endpoints import upload, trim, concat, process, download, info
from app.db.session import Base, engine

app = FastAPI()

Base.metadata.create_all(bind=engine)


origins = ["*"]


router_objects = {}

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload.router, prefix="/api/v1", tags=["upload"])
app.include_router(trim.router, prefix="/api/v1", tags=["trim"])
app.include_router(concat.router, prefix="/api/v1", tags=["concat"])
app.include_router(process.router, prefix="/api/v1", tags=["process"])
app.include_router(download.router, prefix="/api/v1", tags=["download"])
app.include_router(info.router, prefix="/api/v1", tags=["info"])