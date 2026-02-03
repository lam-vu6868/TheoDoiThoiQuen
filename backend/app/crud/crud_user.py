# ========================================
# IMPORTS - THỨ VIỆN CẦN THIẾT
# ========================================

from sqlalchemy.orm import Session
# Session: Đối tượng quản lý connection với database
# Dùng để thực hiện các thao tác CRUD (query, insert, update, delete)

from sqlalchemy import select
# select: Câu lệnh SELECT của SQLAlchemy 2.0 (modern style)
# Thay thế cho query() cũ, dùng để lấy dữ liệu từ database
# Ví dụ: select(User).where(User.id == 1)

from typing import Optional, List
# Optional[Type]: Kiểu dữ liệu có thể None hoặc Type
# List[Type]: Kiểu dữ liệu là danh sách các Type
# Dùng để type hint cho functions (giúp IDE gợi ý code tốt hơn)

from app.models.model import User
# User: Model đại diện cho bảng users trong database
# Chứa các field: id, username, email, hashed_password, full_name, role, created_at

from app.core.security import get_password_hash, verify_password
# get_password_hash(password: str) -> str: Hash password bằng bcrypt trước khi lưu vào DB
# verify_password(plain_password: str, hashed_password: str) -> bool: Kiểm tra password có đúng không


# ========================================
# CODE CÁC FUNCTIONS Ở ĐÂY
# ========================================
# Các functions cần tạo:
# - get_user_by_email(db, email) -> Optional[User]
# - get_user_by_username(db, username) -> Optional[User]
# - get_user_by_id(db, user_id) -> Optional[User]
# - get_users(db, skip, limit) -> List[User]
# - create_user(db, username, email, password, full_name, role) -> User
# - update_user(db, user_id, **kwargs) -> Optional[User]
# - delete_user(db, user_id) -> bool
# - authenticate_user(db, username_or_email, password) -> Optional[User] 