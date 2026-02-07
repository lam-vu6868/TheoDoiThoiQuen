# BaseModel: Class cơ bản của Pydantic để định nghĩa schema/DTO (Data Transfer Object)
# - Tự động validate dữ liệu đầu vào theo kiểu dữ liệu đã khai báo
# - Tự động serialize/deserialize JSON ↔ Python object
# - Dùng để định nghĩa request body, response body trong FastAPI
# - Ví dụ: class UserCreate(BaseModel) để validate dữ liệu khi tạo user mới
from pydantic import BaseModel


# EmailStr: Kiểu dữ liệu đặc biệt của Pydantic để validate email
# - Tự động kiểm tra định dạng email hợp lệ (có @, domain name, etc.)
# - Throw ValidationError nếu email không đúng format
# - Chuẩn hóa email về lowercase
# - Cần cài thêm: pip install "pydantic[email]" hoặc pip install email-validator
# - Ví dụ: email: EmailStr → chỉ chấp nhận "user@example.com", reject "invalid-email"
from pydantic import EmailStr

# Field: Function để thêm metadata và validation rules chi tiết cho từng trường
# - Đặt giá trị min/max length: Field(min_length=3, max_length=50)
# - Đặt pattern regex: Field(pattern=r"^[a-zA-Z0-9_]+$")
# - Thêm description cho API docs: Field(description="Username của người dùng")
# - Đặt ví dụ: Field(example="john_doe")
# - Đặt giá trị mặc định: Field(default="user")
# - Ví dụ: username: str = Field(min_length=3, max_length=20, pattern=r"^[a-zA-Z0-9_]+$")
from pydantic import Field

# field_validator: Decorator để tạo custom validation logic phức tạp (Pydantic v2)
# - Validate theo business logic riêng (VD: password phải có chữ hoa, số, ký tự đặc biệt)
# - Kiểm tra điều kiện giữa các trường với nhau
# - Transform/chuẩn hóa dữ liệu trước khi lưu (VD: strip whitespace, lowercase username)
# - Thay thế cho @validator trong Pydantic v1
# - Ví dụ: @field_validator('password') để check password strength
from pydantic import field_validator

# Optional: Type hint cho các trường có thể là None (không bắt buộc)
# - Optional[str] tương đương str | None
# - Dùng cho các trường không required khi update: full_name: Optional[str] = None
# - Cho phép client không gửi field đó hoặc gửi null
# - Ví dụ: middle_name: Optional[str] = None → có thể bỏ qua khi tạo user
from typing import Optional

# datetime: Kiểu dữ liệu Python chuẩn để làm việc với ngày giờ
# - Dùng cho các trường timestamp: created_at, updated_at, last_login
# - Pydantic tự động parse ISO 8601 string → datetime object
# - Tự động serialize datetime → ISO string trong JSON response
# - Ví dụ: created_at: datetime → FastAPI tự convert "2026-02-07T10:30:00Z"
from datetime import datetime

# validators: Import các hàm validate từ utils
from app.utils.validators import (
    validate_username,
    validate_password_strength,
    validate_full_name
)


# =========  Đăng ký/tạo mới (username, email, password, full_name) ===========
class UserCreate(BaseModel):
    username: str = Field(
        min_length=3, 
        max_length=20,
        description="Tên đăng nhập (3-20 ký tự, chỉ chữ, số, gạch dưới)",
        examples=["john_doe", "user123"]
    )
    email: EmailStr = Field(
        description="Email hợp lệ",
        examples=["user@example.com"]
    )
    password: str = Field(
        min_length=6,
        description="Mật khẩu (tối thiểu 6 ký tự)",
        examples=["MyPass@123"]
    )
    full_name: str = Field(
        min_length=5,
        max_length=50,
        description="Họ và tên đầy đủ",
        examples=["Nguyễn Văn A"]
    )

    # ===== VALIDATOR 1: Validate username =====
    # Gọi hàm validate_username từ utils/validators.py
    @field_validator('username')
    @classmethod
    def check_username(cls, value: str) -> str:
        """Validate username bằng utils validator."""
        return validate_username(value)

    # ===== VALIDATOR 2: Validate password strength =====
    # Gọi hàm validate_password_strength từ utils/validators.py
    @field_validator('password')
    @classmethod
    def check_password(cls, value: str) -> str:
        """Validate password strength bằng utils validator."""
        return validate_password_strength(value)

    # ===== VALIDATOR 3: Validate full_name =====
    # Gọi hàm validate_full_name từ utils/validators.py
    @field_validator('full_name')
    @classmethod
    def check_full_name(cls, value: str) -> str:
        """Validate và chuẩn hóa full_name bằng utils validator."""
        return validate_full_name(value)

# =========== TRẢ DỮ LIỆU VỀ CHO NGƯỜI DÙNG ============
class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    full_name: str
    role: str
    created_at: datetime

    class Config:
        from_attributes = True
