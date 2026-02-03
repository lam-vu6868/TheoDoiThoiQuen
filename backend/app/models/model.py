from sqlalchemy import (
    Column, DateTime, Integer, 
    String, ForeignKey, Float, Date
)

from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


# ==================== BẢNG USER ====================
class User(Base):
    """
    Bảng lưu thông tin người dùng.
    Role lưu trực tiếp dạng string: "admin" hoặc "user"
    """
    __tablename__ = "users"
    
    # --- Cột Primary Key ---
    id = Column(Integer, primary_key=True)
    
    # --- Thông tin đăng nhập ---
    username = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)  # Đã hash
    
    # --- Thông tin cá nhân ---
    full_name = Column(String, nullable=False)
    
    # --- Role (admin hoặc user) ---
    role = Column(String, nullable=False, server_default="user")
    
    # --- Audit fields ---
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # --- Relationships ---
    # Xóa User → Xóa hết Habits và Sessions
    habits = relationship("Habit", back_populates="user", cascade="all, delete-orphan")
    sessions = relationship("UserSession", back_populates="user", cascade="all, delete-orphan")


# ==================== BẢNG USER SESSION ====================
class UserSession(Base):
    """
    Bảng theo dõi sessions đăng nhập.
    Dùng để giới hạn số đăng nhập không cho đăng nhập 2 nơi 1 lúc
    hoặc khi đăng nhập nới này
    thì đăng xuất bên kia 
    , force logout, theo dõi hoạt động.
    """
    __tablename__ = "user_sessions"
    
    # --- Cột Primary Key ---
    id = Column(Integer, primary_key=True)
    
    # --- Foreign Key đến User ---
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # --- JWT ID (jti claim trong JWT) ---
    jti = Column(String, unique=True, nullable=False, index=True)
    
    # --- Thời gian ---
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=False)
    
    # --- Relationship ---
    user = relationship("User", back_populates="sessions")


# ==================== BẢNG HABIT CATEGORY ====================
class HabitCategory(Base):
    """
    Bảng danh mục thói quen.
    VD: Sức khỏe, Học tập, Công việc, Thể thao...
    """
    __tablename__ = "habit_categories"
    
    # --- Cột Primary Key ---
    id = Column(Integer, primary_key=True)
    
    # --- Tên và mô tả ---
    name = Column(String, unique=True, nullable=False)
    desc = Column(String, nullable=True)
    
    # --- Relationship ---
    habits = relationship("Habit", back_populates="category")


# ==================== BẢNG HABIT ====================
class Habit(Base):
    """
    Bảng lưu thói quen của user.
    VD: Chạy bộ 5km, Đọc sách 30 trang, Uống 2L nước...
    """
    __tablename__ = "habits"
    
    # --- Cột Primary Key ---
    id = Column(Integer, primary_key=True)
    
    # --- Foreign Keys ---
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    category_id = Column(Integer, ForeignKey("habit_categories.id"), nullable=False, index=True)
    
    # --- Thông tin habit ---
    name = Column(String, nullable=False)  # "Chạy bộ", "Đọc sách"
    desc = Column(String, nullable=True)   # Mô tả chi tiết
    
    # --- Tần suất (ngày nào trong tuần) ---
    # Mảng số: [0, 2, 4] = Thứ 2, Thứ 4, Thứ 6
    # 0=Monday, 1=Tuesday, ..., 6=Sunday
    frequency = Column(ARRAY(Integer), nullable=False)
    
    # --- Mục tiêu ---
    unit = Column(String, nullable=True)          # "km", "trang", "ly nước"
    target_value = Column(Float, nullable=True)   # 5.0, 30, 2.0
    
    # --- Giao diện ---
    color = Column(String, nullable=True)  # Mã màu HEX: "#FF5733"
    
    # --- Audit ---
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # --- Relationships ---
    user = relationship("User", back_populates="habits")
    category = relationship("HabitCategory", back_populates="habits")
    # Xóa Habit → Xóa hết Logs
    habit_logs = relationship("HabitLog", back_populates="habit", cascade="all, delete-orphan")


# ==================== BẢNG HABIT LOG ====================
class HabitLog(Base):
    """
    Bảng nhật ký check-in thói quen.
    Lưu kết quả thực hiện hàng ngày.
    """
    __tablename__ = "habit_logs"
    
    # --- Cột Primary Key ---
    id = Column(Integer, primary_key=True)
    
    # --- Foreign Key ---
    habit_id = Column(Integer, ForeignKey("habits.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # --- Kết quả thực hiện ---
    value = Column(Float, nullable=True)  # Kết quả: 5.2km, 25 trang...
    status = Column(String, nullable=False)  # "COMPLETED", "SKIPPED", "FAILED"
    
    # --- Ngày ---
    record_date = Column(Date, nullable=False, index=True)  # Ngày logic (2026-02-02)
    
    # --- Audit ---
    created_at = Column(DateTime(timezone=True), server_default=func.now())  # Thời điểm check-in
    
    # --- Relationship ---
    habit = relationship("Habit", back_populates="habit_logs")


# ==================== BẢNG MOTIVATION QUOTE ====================
class MotivationQuote(Base):
    """
    Bảng lưu câu trích dẫn động viên.
    Hiển thị random mỗi ngày cho user.
    """
    __tablename__ = "motivation_quotes"
    
    # --- Cột Primary Key ---
    id = Column(Integer, primary_key=True)
    
    # --- Nội dung ---
    quote = Column(String, nullable=False)  # "Success is not final..."
    author = Column(String, nullable=True)  # "Winston Churchill"
 
