from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Tạo engine kết nối database
engine = create_engine(
    settings.DATABASE_URL,
    # Không cần check_same_thread vì dùng PostgreSQL
    pool_pre_ping=True  # Kiểm tra connection trước khi dùng
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class cho tất cả models
Base = declarative_base()


# Dependency để lấy database session
def get_db():
    """
    Tạo database session cho mỗi request
    Tự động đóng sau khi xong
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
