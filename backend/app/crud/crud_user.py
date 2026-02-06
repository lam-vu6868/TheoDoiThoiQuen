# ========================================
# IMPORTS - THƯ VIỆN CẦN THIẾT (ASYNC VERSION)
# ========================================

from sqlalchemy.ext.asyncio import AsyncSession
# AsyncSession: Đối tượng quản lý async connection với database
# Thay thế Session sync, hỗ trợ await cho query/insert/update/delete
# Dùng với: await db.execute(), await db.commit()

from sqlalchemy import select
# select: Câu lệnh SELECT của SQLAlchemy 2.0 (modern style)
# Thay thế cho query() cũ, dùng để lấy dữ liệu từ database
# Ví dụ: select(User).where(User.id == 1)
# Dùng chung cho cả sync và async

from typing import Optional, List
# Optional[Type]: Kiểu dữ liệu có thể None hoặc Type
# List[Type]: Kiểu dữ liệu là danh sách các Type
# Dùng để type hint cho functions (giúp IDE gợi ý code tốt hơn)

from app.models.model import User as u 
# User: Model đại diện cho bảng users trong database
# Chứa các field: id, username, email, hashed_password, full_name, role, created_at

from app.core.security import get_password_hash, verify_password
# get_password_hash(password: str) -> str: Hash password bằng bcrypt trước khi lưu vào DB
# verify_password(plain_password: str, hashed_password: str) -> bool: Kiểm tra password có đúng không


# ========================================
# CODE CÁC FUNCTIONS Ở ĐÂY (ASYNC VERSION)
# ========================================
# Các functions cần tạo (tất cả đều async):
# - get_user_by_email(db, email) -> Optional[User]
# - get_user_by_username(db, username) -> Optional[User]
# - get_user_by_id(db, user_id) -> Optional[User]
# - get_users(db, skip, limit) -> List[User]
# - create_user(db, username, email, password, full_name, role) -> User
# - update_user(db, user_id, **kwargs) -> Optional[User]
# - delete_user(db, user_id) -> bool
# - authenticate_user(db, username_or_email, password) -> Optional[User]


async def get_user_by_email(db: AsyncSession, email:str) -> Optional[u]:
    """
    Tìm user theo email (ASYNC VERSION)
    
    Args:
        db: AsyncSession - Database session bất đồng bộ
        email: str - Email cần tìm
        
    Returns:
        Optional[User] - User object nếu tìm thấy, None nếu không tìm thấy
        
    Cách dùng trong endpoint:
        user = await get_user_by_email(db, "test@example.com")
        if user:
            print(user.username)
    """
    # Bước 1: Tạo câu query SELECT
    stmt = select(u).where(u.email == email)
    # select(User): SELECT * FROM users
    # where(User.email == email): WHERE email = 'email'
    # stmt là statement object (chưa thực thi)
    
    # Bước 2: Thực thi query với await (async)
    result = await db.execute(stmt)
    # await: Chờ database trả kết quả (non-blocking)
    # Trong lúc chờ, server có thể xử lý request khác
    # result: Result object chứa dữ liệu trả về
    
    # Bước 3: Lấy user đầu tiên (hoặc None)
    user = result.scalar_one_or_none()
    # scalar_one_or_none(): Lấy 1 object duy nhất hoặc None
    # Nếu có nhiều hơn 1 kết quả → raise Exception
    # Nếu không có kết quả → return None
    
    return user



# 4. create_user(db, username, email, password, full_name, role):
#    - hashed_password = get_password_hash(password)
#    - new_user = User(username=username, email=email, ...)
#    - db.add(new_user)
#    - await db.commit()  # ← Phải có await
#    - await db.refresh(new_user)  # ← Phải có await
#    - return new_user

# 5. update_user(db, user_id, **kwargs):
#    - user = await get_user_by_id(db, user_id)
#    - if not user: return None
#    - for key, value in kwargs.items():
#    -     setattr(user, key, value)
#    - await db.commit()
#    - await db.refresh(user)
#    - return user

# 6. delete_user(db, user_id):
#    - user = await get_user_by_id(db, user_id)
#    - if not user: return False
#    - await db.delete(user)
#    - await db.commit()
#    - return True

# 7. authenticate_user(db, username_or_email, password):
#    - user = await get_user_by_email(db, username_or_email)
#    - if not user:
#    -     user = await get_user_by_username(db, username_or_email)
#    - if not user: return None
#    - if not verify_password(password, user.hashed_password):
#    -     return None
#    - return user



# |===================================
# |     LẤY THEO TÊN ĐĂNG NHẬP        
# |===================================
async def get_user_by_username(db: AsyncSession, userName:str)-> Optional[u]:
    # Chuẩn bị lệnh để thực thi 
    stmt = select(u).where(u.username == userName)

    # Thực thi lệnh 
    result = await db.execute(stmt)

    # Lấy user đầu tiên
    user = result.scalar_one_or_none()

    # Nếu có trả về user, không có trả về none
    return user


# |===================================
# |       LẤY THEO USER ID              
# |===================================
async def get_user_by_id (db: AsyncSession , user_id:int) -> Optional[u]:

    stmt = select(u).where(u.id == user_id)

    result = await db.execute(stmt)

    user = result.scalar_one_or_none()

    return user


# |===================================
# |       LẤY THEO LIST USER              
# |===================================
async def get_user(db: AsyncSession , skip:int, limit:int) -> List[u]:
    """
        Mục đích hàm này dùng để phân phân trang
    """
    stmt = select(u).offset(skip).limit(limit)

    result = await db.execute(stmt) 

    users = result.scalars().all() 

    return users 


# |===================================
# |        TẠO USER MỚI              
# |===================================
async def create_user(db:AsyncSession, full_name:str, username:str, password:str, email:str):
    pass 











    