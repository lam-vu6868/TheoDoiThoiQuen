from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import decode_access_token

# OAuth2PasswordBearer để lấy token từ header "Authorization: Bearer <token>"
# tokenUrl: đường dẫn API login (Swagger dùng để hiển thị nút Authorize)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    """
    Dependency để lấy thông tin user hiện tại từ JWT token
    
    Cách dùng trong router:
        @app.get("/profile")
        def get_profile(current_user = Depends(get_current_user)):
            return {"user": current_user}
    
    Args:
        token: JWT token từ header Authorization
        db: Database session
        
    Returns:
        User object từ database
        
    Raises:
        HTTPException 401: Nếu token không hợp lệ hoặc user không tồn tại
    """
    # Giải mã token để lấy user_id
    payload = decode_access_token(token)
    
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token không hợp lệ hoặc đã hết hạn",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user_id: int = payload.get("user_id")
    
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token không chứa user_id",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Import User model (import ở đây để tránh circular import)
    from backend.app.models.model import User
    
    # Lấy user từ database
    user = db.query(User).filter(User.id == user_id).first()
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User không tồn tại",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user
