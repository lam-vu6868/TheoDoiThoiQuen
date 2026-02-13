from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from typing import Optional
from datetime import datetime
from app.models.model import UserSession as us


# ==============================
#   Lấy Session theo user_id
# ==============================
async def get_session(db: AsyncSession, user_id: int) -> Optional[us]:
    """Lấy session của user (nếu có)"""
    stmt = select(us).where(us.user_id == user_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


# ========================
#   Xóa Session theo user_id
# ========================
async def delete_session(db: AsyncSession, user_id: int) -> bool:
    """
    Xóa tất cả sessions của user theo user_id.
    Dùng khi đăng nhập mới → đảm bảo chỉ 1 session active.
    """
    stmt = delete(us).where(us.user_id == user_id)
    result = await db.execute(stmt)
    await db.commit()
    # result.rowcount = số dòng đã xóa, > 0 nghĩa là có xóa
    return result.rowcount > 0


# ============================================================
# TODO: Thêm hàm get_session_by_jti
# ============================================================
async def get_session_by_jti(db: AsyncSession, jti: str) -> Optional[us]:
    """
    Tìm session theo jti (JWT ID).
    Dùng trong dependencies.py để verify token còn hợp lệ không.
    
    Flow: decode token → lấy jti → gọi hàm này → có = OK, không = bị đá
    """
    stmt = select(us).where(us.jti == jti)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()



# ==============================
#   Tạo Session mới
# ==============================
async def create_session(db: AsyncSession, user_id: int, jti: str, expires_at: datetime) -> us:
    """
    Tạo session mới cho user sau khi đăng nhập thành công.
    Lưu jti (JWT ID) vào DB để sau này verify token có còn hợp lệ không.
    
    Args:
        user_id: ID của user vừa đăng nhập
        jti: JWT ID unique (từ create_access_token) → dùng để đối chiếu token
        expires_at: Thời điểm token hết hạn
    
    Returns:
        UserSession object vừa tạo
    """
    new_session = us(
        user_id=user_id,
        jti=jti,
        expires_at=expires_at
    )
    db.add(new_session)
    await db.commit()
    await db.refresh(new_session)
    return new_session

