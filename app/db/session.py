from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLAlchemy 사용할 DB URL 생성하기
SQLALCHEMY_DATABASE_URL = "sqlite:///./sqlite3.db"

# SQLAlchemy engine 생성하기
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# DB 세션 생성하기
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class 생성하기
Base = declarative_base()