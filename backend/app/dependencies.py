from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
# AsyncSession: Database session bất đồng bộ (thay Session sync)
# Hỗ trợ await cho các operations: execute(), commit(), refresh()

from sqlalchemy import select
# select: Câu lệnh SELECT của SQLAlchemy 2.0
# Thay thế db.query() cũ (SQLAlchemy 1.x)

from app.core.database import get_db
from app.core.security import decode_access_token
from app.crud.crud_session import get_session_by_jti

# OAuth2PasswordBearer để lấy token từ header "Authorization: Bearer <token>"
# tokenUrl: đường dẫn API login (Swagger dùng để hiển thị nút Authorize)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
):
    """
    Dependency để lấy thông tin user hiện tại từ JWT token (ASYNC VERSION)
    
    Cách dùng trong router:
        @app.get("/profile")
        async def get_profile(current_user = Depends(get_current_user)):
            return {"user": current_user}
    
    Args:
        token: JWT token từ header Authorization
        db: AsyncSession - Database session bất đồng bộ
        
    Returns:
        User object từ database
        
    Raises:
        HTTPException 401: Nếu token không hợp lệ hoặc user không tồn tại
    """
    # Bước 1: Giải mã token để lấy user_id
    payload = decode_access_token(token)
    
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token không hợp lệ hoặc đã hết hạn",
            headers={"WWW-Authenticate": "Bearer"},
        )
    

    # ============================================================
    # BƯỚC 2: Lấy jti (JWT ID) từ payload token
    # jti là "số seri" của token, dùng để check trong DB còn hợp lệ không
    # ============================================================
    jti = payload.get("jti")
    
    if jti is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token không hợp lệ",
            headers={"WWW-Authenticate": "Bearer"},
        )
    

    # ============================================================
    # TODO 2: Kiểm tra jti có trong bảng user_sessions không
    # - Import hàm get_session_by_jti từ crud_session (cần tạo hàm này)
    # - Gọi: session = await get_session_by_jti(db, jti)
    # - Nếu session là None → raise 401 "Phiên đăng nhập đã hết hạn hoặc đã đăng nhập nơi khác"
    # - Mục đích: nếu user đăng nhập nơi khác → jti cũ bị xóa → token cũ bị chặn
    # ============================================================
    existing_jti = await get_session_by_jti(db, jti)

    if not existing_jti:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Phiên đăng nhập đã hết hạn hoặc đã đăng nhập nơi khác"
        ) 

    # TODO 3: Sửa lại dòng dưới - payload dùng "sub" chứ không phải "user_id"
    # - Hiện tại: user_id = payload.get("user_id")  ← SAI, token lưu là "sub"
    # - Sửa thành: user_id = payload.get("sub")
    # - Rồi convert: user_id = int(user_id) vì sub lưu dạng string
    user_id: int = payload.get("sub")
    

    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token không chứa user_id",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Bước 2: Import User model (import ở đây để tránh circular import)
    from app.models.model import User
    
    # Bước 3: Lấy user từ database (ASYNC)
    # CŨ (SQLAlchemy 1.x): user = db.query(User).filter(User.id == user_id).first()
    # MỚI (SQLAlchemy 2.0):
    stmt = select(User).where(User.id == user_id)
    result = await db.execute(stmt)  # ← Phải có await
    user = result.scalar_one_or_none()
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User không tồn tại",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user
