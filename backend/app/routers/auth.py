
from fastapi import HTTPException, Depends, APIRouter, status

from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import UserCreate, UserResponse,UserLogin
from app.crud.crud_user import (
    create_user,           # Tạo user mới trong DB
    get_user_by_email,     # Kiểm tra email đã tồn tại chưa
    get_user_by_username   # Kiểm tra username đã tồn tại chưa
)
from app.crud.crud_session import delete_session, get_session, create_session
from app.core.database import get_db
from app.core.security import hash_password, verify_password, create_access_token, decode_access_token
from app.dependencies import get_current_user, oauth2_scheme
from app.schemas.user import ForgotPasswordRequest, ResetPasswordRequest
from app.crud.crud_user import get_user_by_email, update_user
from app.utils.email import send_password_reset_email
from datetime import timedelta


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



# ========================================
# ENDPOINT: ĐĂNG NHẬP TÀI KHOẢN
# ========================================
@router.post(
    "/login",
    summary="Đăng nhập tài khoản",
    description="Đăng nhập bằng username/email và password",
    status_code=status.HTTP_200_OK
)
async def login(user: UserLogin ,db: AsyncSession = Depends(get_db)):

   
    # Kiểm tra có username không 
    existing_name_email = await get_user_by_username(db=db , username=user.username_or_email)

    # Nếu không có thì kiểm tra email 
    if not existing_name_email:
        existing_name_email = await get_user_by_email(db=db, email=user.username_or_email)

    if not existing_name_email:
         raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Tài khoản hoặc mật khẩu không chính xác"
         )
    
    # Kiểm tra mật khẩu 
    check_pw = verify_password(plain_password=user.password, hashed_password=existing_name_email.password)

    if not check_pw:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Tài khoản hoặc mật khẩu không chính xác"
        )
    
    # |=============================================
    # | BƯỚC 3: KIỂM TRA & XÓA SESSION CŨ (SINGLE SESSION)
    # |=============================================
    # Kiểm tra người dùng này có session (token) trong db không
    existing_session = await get_session(db, existing_name_email.id)

    # Nếu có → xóa session cũ đi (user chỉ được đăng nhập 1 nơi)
    if existing_session:
        await delete_session(db, existing_name_email.id)

    # |=============================================
    # | BƯỚC 4: TẠO TOKEN MỚI + LƯU SESSION
    # |=============================================
    
    # Gọi create_access_token để tạo JWT token
    # - data={"sub": "1"}: payload chứa user_id ("sub" là subject - chuẩn JWT)
    # - Trả về 3 giá trị:
    #   + access_token: chuỗi JWT gửi cho client (VD: "eyJhbGciOiJIUzI1NiIs...")
    #   + jti: JWT ID unique (VD: "a1b2c3d4-e5f6-...") → lưu vào DB để track
    #   + expires_at: thời điểm hết hạn (VD: 2026-02-13 10:30:00)
    access_token, jti, expires_at = create_access_token(
        data={"sub": str(existing_name_email.id)}
    )
    
    # Lưu session mới vào bảng user_sessions
    # Mục đích: khi verify token sau này, kiểm tra jti có trong DB không
    # Nếu jti không có (bị xóa do đăng nhập nơi khác) → token không hợp lệ 
    await create_session(
        db=db,
        user_id=existing_name_email.id,  # User nào
        jti=jti,                          # Token nào (đối chiếu khi verify)
        expires_at=expires_at             # Hết hạn lúc nào
    )
    
    # |=============================================
    # | BƯỚC 5: TRẢ VỀ TOKEN CHO CLIENT
    # |=============================================
    # Client sẽ lưu access_token vào localStorage hoặc cookie
    # Mỗi request sau này gửi kèm header: Authorization: Bearer <access_token>
    return {
        "access_token": access_token,
        "token_type": "bearer"  # Chuẩn OAuth2: cho client biết loại token
    }



@router.post(
    "/forgot-password",
    summary="Yêu cầu đặt lại mật khẩu",
    status_code=status.HTTP_200_OK,
)
async def forgot_password(request: ForgotPasswordRequest, db: AsyncSession = Depends(get_db)):
    """
    Gửi email chứa link/ token để reset mật khẩu.
    Quy trình:
      - Nếu email tồn tại: tạo reset token (mục đích password_reset) và gửi mail
      - Trả về 200 luôn để tránh lộ thông tin email tồn tại
    """
    user = await get_user_by_email(db, request.email)
    if user:
        # Tạo token có mục đích rõ ràng và thời gian ngắn
        reset_token, jti, expires_at = create_access_token(
            data={"sub": str(user.id), "purpose": "password_reset"},
            expires_delta=timedelta(minutes=15),
        )
        # Gửi email (async)
        try:
            await send_password_reset_email(user.email, reset_token)
        except Exception:
            # Ghi log/ignore lỗi gửi mail nhưng không báo chi tiết cho client
            pass

    return {"message": "Nếu email tồn tại, chúng tôi đã gửi hướng dẫn đặt lại mật khẩu"}



@router.post(
    "/reset-password",
    summary="Đặt lại mật khẩu",
    status_code=status.HTTP_200_OK,
)
async def reset_password(request: ResetPasswordRequest, db: AsyncSession = Depends(get_db)):
    """
    Reset mật khẩu bằng token gửi qua email.
    Flow:
      - Decode token, kiểm tra purpose == 'password_reset'
      - Lấy user_id từ sub
      - Hash mật khẩu mới và cập nhật DB
      - Xóa sessions cũ để logout tất cả thiết bị
    """
    payload = decode_access_token(request.token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Token không hợp lệ hoặc đã hết hạn")

    purpose = payload.get("purpose")
    if purpose != "password_reset":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Token không hợp lệ")

    sub = payload.get("sub")
    if sub is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Token không chứa user")

    user_id = int(sub)

    # Hash password và cập nhật
    new_hashed = hash_password(request.new_password)
    updated = await update_user(db, user_id, password=new_hashed)
    if not updated:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User không tồn tại")

    # Xóa session cũ (force logout)
    await delete_session(db, user_id)

    return {"message": "Đổi mật khẩu thành công"}


# ========================================
# ENDPOINT: ĐĂNG XUẤT TÀI KHOẢN
# ========================================
@router.post(
    "/logout", 
    summary="Đăng xuất tài khoản",
    description="Vô hiệu hóa phiên làm việc bằng cách xóa jti trong database",
    status_code=status.HTTP_200_OK
)

async def logout(
    # Depends(get_current_user): tự động verify token + check jti trong DB
    # Nếu token hợp lệ → trả về User object
    # Nếu không → tự raise 401 (không cần xử lý ở đây)
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Endpoint đăng xuất tài khoản
    
    **Flow xử lý:**
    1. get_current_user verify token → đảm bảo user đang đăng nhập
    2. Xóa session của user trong bảng user_sessions
    3. Token cũ sẽ bị vô hiệu hóa (jti không còn trong DB)
    
    **Headers required:**
    - Authorization: Bearer <access_token>
    
    **Returns:**
    - {"message": "Đăng xuất thành công"}
    """
    
    # |=============================================
    # | BƯỚC 1: XÓA SESSION TRONG DB
    # |=============================================
    # current_user đã được verify bởi get_current_user dependency
    # → chắc chắn user hợp lệ và đang có session active
    # Xóa session → jti bị xóa khỏi DB → token cũ không dùng được nữa
    await delete_session(db, current_user.id)
    
    # |=============================================
    # | BƯỚC 2: TRẢ VỀ THÔNG BÁO
    # |=============================================
    return {"message": "Đăng xuất thành công"}




















