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

from app.core.security import verify_password, get_password_hash
# get_password_hash(password: str) -> str: Hash password bằng bcrypt trước khi lưu vào DB
# verify_password(plain_password: str, hashed_password: str) -> bool: Kiểm tra password có đúng không




# |===================================
# |     LẤY THEO USER THEO EMAIL        
# |===================================
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
async def create_user(db:AsyncSession, full_name:str, username:str, password:str, email:str, role:str="user") -> u:
    """
    Tạo user mới trong database.
    Không validate dữ liệu - validation phải làm ở router layer.
    
    Args:
        db: AsyncSession
        full_name: Tên đầy đủ
        username: Tên đăng nhập (unique)
        password: Password dạng plain text (sẽ được hash)
        email: Email (unique)
        role: Role của user ("user" hoặc "admin"), mặc định "user"
        
    Returns:
        User object vừa tạo (có id và created_at từ DB)
    """
    
    # Bước 2: Tạo User object
    new_user = u(
        username=username,
        email=email,
        password=password,
        full_name=full_name,
        role=role
    )
    
    # Bước 3: Thêm vào session
    db.add(new_user)
    
    # Bước 4: Commit vào database
    await db.commit()
    
    # Bước 5: Refresh để lấy id và created_at từ DB
    await db.refresh(new_user)
    
    # Bước 6: Trả về user mới
    return new_user




# |===================================
# |        CẬP NHẬT USER               
# |===================================
async def update_user(db: AsyncSession, user_id: int, **kwargs) -> Optional[u]:
    """
    Cập nhật thông tin user.
    Chỉ cập nhật các field được truyền vào **kwargs.
    
    Args:
        db: AsyncSession
        user_id: ID của user cần cập nhật
        **kwargs: Các field cần cập nhật
                  Ví dụ: full_name="John", email="new@email.com"
        
    Returns:
        User object đã cập nhật, hoặc None nếu không tìm thấy
        
    Ví dụ:
        user = await update_user(db, 1, full_name="John Doe", email="john@new.com")
    """
    # Bước 1: Tìm user theo ID
    user = await get_user_by_id(db, user_id)
    
    # Bước 2: Kiểm tra user có tồn tại không
    if user is None:
        return None  # Không tìm thấy user
    
    # Bước 3: Cập nhật các field từ kwargs
    for key, value in kwargs.items():  # ← Phải có () sau items
        setattr(user, key, value)
        # setattr(user, "full_name", "John") = user.full_name = "John"
    
    # Bước 4: Lưu thay đổi vào database
    await db.commit()
    
    # Bước 5: Refresh để đồng bộ dữ liệu (optional)
    await db.refresh(user)
    
    # Bước 6: Trả về user đã cập nhật
    return user




# |===================================
# |        XÓA USER               
# |===================================
async def delete_user(db: AsyncSession, user_id: int)-> bool:

    user = await get_user_by_id(db,user_id)

    if user is None: 
        return False 

    await db.delete(user)
    await db.commit()

    return True




# |===================================
# |        HÀM XÁC THỰC ĐĂNG NHẬP              
# |===================================
async def authenticate_user(db: AsyncSession, username_or_email: str, password: str) -> Optional[u]:
    """
    Xác thực user khi đăng nhập.
    Cho phép đăng nhập bằng username HOẶC email.
    
    Args:
        db: AsyncSession
        username_or_email: Username hoặc email để đăng nhập
        password: Password dạng plain text (chưa hash)
        
    Returns:
        User object nếu xác thực thành công, None nếu sai thông tin
        
    Ví dụ:
        user = await authenticate_user(db, "john@mail.com", "123456")
        if user:
            # Đăng nhập thành công
            access_token = create_access_token(user.id)
        else:
            # Sai username/email hoặc password
            raise HTTPException(401, "Sai thông tin đăng nhập")
    """
    # Bước 1: Thử tìm user theo email trước
    user = await get_user_by_email(db, username_or_email)
    
    # Bước 2: Nếu không tìm thấy → thử tìm theo username
    if user is None:
        user = await get_user_by_username(db, username_or_email)
    
    # Bước 3: Vẫn không tìm thấy → sai username/email
    if user is None:
        return None  # Không tồn tại user
    
    # Bước 4: Kiểm tra password có đúng không
    if not verify_password(password, user.password):
        return None  # Sai password
    
    # Bước 5: Đúng cả username/email và password
    return user  # Trả về user object để dùng luôn 
    
    






    