# BaseSettings: Class đặc biệt để tự động đọc file .env và validate dữ liệu
from pydantic_settings import BaseSettings 

class Settings(BaseSettings):
    """Cấu hình ứng dụng từ file .env"""
    
    # Database
    DATABASE_URL: str
    
    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    
    # CORS
    FRONTEND_URL: str = "http://localhost:5500"
    
    # App Config (có giá trị mặc định, không bắt buộc trong .env)
    PROJECT_NAME: str = "Habit Tracker API"  # Hiển thị trong Swagger do cs
    DEBUG: bool = True  # True = hiện lỗi chi tiết (dev), False = ẩn lỗi (production)
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Instance duy nhất dùng trong toàn bộ app
settings = Settings()
