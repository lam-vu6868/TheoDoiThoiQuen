
from fastapi import HTTPException, Depends, APIRouter, status

from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import UserCreate, UserResponse 
from app.crud.crud_user import (
    create_user,           # Tạo user mới trong DB
    get_user_by_email,     # Kiểm tra email đã tồn tại chưa
    get_user_by_username   # Kiểm tra username đã tồn tại chưa
)
from app.core.database import get_db
from app.core.security import hash_password


# ========================================
# ROUTER CONFIGURATION
# ========================================
router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


# ========================================
# ENDPOINT: ĐĂNG KÝ TÀI KHOẢN MỚI
# ========================================
@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Đăng ký tài khoản mới",
    description="Tạo tài khoản user mới với username, email, password và full_name"
)
async def register(
    user: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Endpoint đăng ký tài khoản mới
    
    **Flow xử lý:**
    1. Validate dữ liệu đầu vào (tự động bởi UserCreate schema)
    2. Kiểm tra username đã tồn tại chưa → Lỗi 400 nếu trùng
    3. Kiểm tra email đã tồn tại chưa → Lỗi 400 nếu trùng
    4. Hash password bằng bcrypt
    5. Tạo user mới trong database
    6. Trả về thông tin user vừa tạo (không bao gồm password)
    
    **Args:**
    - user (UserCreate): Request body chứa:
        - username: 3-20 ký tự, chỉ chữ, số, gạch dưới
        - email: Email hợp lệ
        - password: Tối thiểu 6 ký tự
        - full_name: Họ tên đầy đủ 5-50 ký tự
        
    **Returns:**
    - UserResponse: Thông tin user vừa tạo (id, username, email, full_name, role, created_at)
    
    **Raises:**
    - 400 Bad Request: Username hoặc email đã tồn tại
    - 500 Internal Server Error: Lỗi database
    """
    
    # |=======================================
    # | BƯỚC 1: KIỂM TRA USERNAME ĐÃ TỒN TẠI
    # |=======================================
    existing_username = await get_user_by_username(db, user.username)
    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Tên đăng nhập đã tồn tại."
        )
    
    # |===================================
    # | BƯỚC 2: KIỂM TRA EMAIL ĐÃ TỒN TẠI
    # |===================================
    existing_email = await get_user_by_email(db, user.email)
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Email '{user.email}' đã được đăng ký. Vui lòng sử dụng email khác hoặc đăng nhập."
        )
    
    # |===================================
    # | BƯỚC 3: MÃ HÓA PASSWORD
    # |===================================
    hashed_password = hash_password(user.password)
    # Input: "MyPass@123" (plain text)
    # Output: "$2b$12$xyz...abc" (hashed - không thể giải mã ngược)
    
    # |===================================
    # | BƯỚC 4: TẠO USER MỚI TRONG DATABASE
    # |===================================
    new_user = await create_user(
        db=db,
        username=user.username,
        email=user.email,
        password=hashed_password,  # ← Lưu password đã hash, KHÔNG lưu plain text
        full_name=user.full_name,
        role="user"  # Mặc định role là "user" (không phải admin)
    )
    
    # |===================================
    # | BƯỚC 5: TRẢ VỀ THÔNG TIN USER
    # |===================================
    # FastAPI tự động serialize new_user thành UserResponse
    # Không trả về password (UserResponse không có field password)
    return new_user


