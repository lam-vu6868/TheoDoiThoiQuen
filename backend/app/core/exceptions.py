# ============================================================================
# FILE: exceptions.py
# MỤC ĐÍCH: Centralized Exception Handling - Xử lý lỗi tập trung cho toàn bộ API
# ============================================================================
# Khi FastAPI/Pydantic phát hiện lỗi validation (VD: username quá ngắn, email sai format),
# nó tự động raise RequestValidationError với message TIẾNG ANH.
# File này sẽ CHẶN (intercept) các lỗi đó và CHUYỂN ĐỔI sang tiếng Việt
# trước khi trả về cho client (frontend).
# ============================================================================

from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from typing import Dict, Any


# ============================================================================
# BẢNG MAP LỖI: Ánh xạ từ error_type + field_name → Message tiếng Việt
# ============================================================================
# Cấu trúc: {"error_type": {"field_name": "Message template"}}
# - error_type: Loại lỗi mà Pydantic trả về (VD: string_too_short, value_error)
# - field_name: Tên trường bị lỗi (VD: username, email, password)
# - Message template: Có thể chứa {placeholder} để điền giá trị động từ error.ctx
#   VD: {min_length}, {max_length}, {pattern}
# ============================================================================

VALIDATION_MESSAGES: Dict[str, Dict[str, str]] = {
    # ===== LỖI STRING QUÁ NGẮN =====
    # Khi Field(min_length=3) mà user nhập ít hơn 3 ký tự
    # error.ctx sẽ có: {"min_length": 3}
    "string_too_short": {
        "username": "Tên đăng nhập phải có ít nhất {min_length} ký tự",
        "password": "Mật khẩu phải có ít nhất {min_length} ký tự",
        "full_name": "Họ và tên phải có ít nhất {min_length} ký tự",
    },
    
    # ===== LỖI STRING QUÁ DÀI =====
    # Khi Field(max_length=20) mà user nhập quá 20 ký tự
    # error.ctx sẽ có: {"max_length": 20}
    "string_too_long": {
        "username": "Tên đăng nhập không được vượt quá {max_length} ký tự",
        "password": "Mật khẩu không được vượt quá {max_length} ký tự",
        "full_name": "Họ và tên không được vượt quá {max_length} ký tự",
    },
    
    # ===== LỖI FIELD BẮT BUỘC (MISSING) =====
    # Khi client không gửi field required (VD: thiếu username trong request body)
    "missing": {
        "username": "Tên đăng nhập là bắt buộc",
        "email": "Email là bắt buộc",
        "password": "Mật khẩu là bắt buộc",
        "full_name": "Họ và tên là bắt buộc",
    },
    
    # ===== LỖI VALIDATION TỪ CUSTOM VALIDATOR =====
    # Khi validator raise ValueError("message") hoặc validation logic thất bại
    # Pydantic sẽ tự động format: "Value error, {message}"
    # Trong trường hợp này, ta để nó giữ nguyên message vì đã là tiếng Việt
    "value_error": {
        # Không cần map vì ValueError đã có message tiếng Việt từ validator
        # VD: raise ValueError("Tên đăng nhập chỉ được chứa chữ, số và gạch dưới")
    },
    
    # ===== LỖI EMAIL KHÔNG HỢP LỆ =====
    # Khi dùng EmailStr mà user nhập email sai format (VD: "abc@", "test")
    "value_error.email": {
        "email": "Email không hợp lệ. Vui lòng nhập đúng định dạng email"
    },
    
    # ===== LỖI KIỂU DỮ LIỆU SAI =====
    # Khi field mong đợi int nhưng nhận được string, hoặc ngược lại
    "int_parsing": {
        "id": "ID phải là số nguyên",
        "age": "Tuổi phải là số nguyên"
    },
    
    "string_type": {
        "username": "Tên đăng nhập phải là chuỗi ký tự",
        "password": "Mật khẩu phải là chuỗi ký tự",
        "full_name": "Họ và tên phải là chuỗi ký tự"
    },
    
    # ===== LỖI PATTERN (REGEX) KHÔNG KHỚP =====
    # Khi Field(pattern=r"^[a-zA-Z0-9_]+$") mà input không match
    "string_pattern_mismatch": {
        "username": "Tên đăng nhập chỉ được chứa chữ cái, số và dấu gạch dưới",
        "phone": "Số điện thoại không đúng định dạng"
    }
}


# ============================================================================
# EXCEPTION HANDLER: Hàm xử lý lỗi validation
# ============================================================================
# Đây là "bộ chặn" chính - mọi RequestValidationError trong API sẽ đi qua đây
# FastAPI tự động gọi hàm này khi có lỗi validation
# 
# FLOW:
# 1. User gửi request với data sai (VD: username có 1 ký tự)
# 2. Pydantic validate → phát hiện lỗi → raise RequestValidationError
# 3. FastAPI chặn exception → GỌI HÀM NÀY thay vì trả lỗi mặc định
# 4. Hàm này biến đổi error → trả về JSONResponse tiếng Việt
# ============================================================================

async def validation_exception_handler(
    request: Request, 
    exc: RequestValidationError
) -> JSONResponse:
    """
    Custom exception handler để chuyển đổi validation errors sang tiếng Việt.
    
    Args:
        request: FastAPI Request object (thông tin về HTTP request)
        exc: RequestValidationError được Pydantic raise
            - exc.errors() trả về list các lỗi dạng:
              [
                {
                  "type": "string_too_short",
                  "loc": ["body", "username"],  # Location: body.username
                  "msg": "String should have at least 3 characters",
                  "input": "ab",
                  "ctx": {"min_length": 3}
                }
              ]
    
    Returns:
        JSONResponse với status 422 và errors đã được dịch sang tiếng Việt
    """
    
    # ===== BƯỚC 1: Khởi tạo mảng chứa errors đã format =====
    translated_errors = []
    
    # ===== BƯỚC 2: Duyệt qua từng lỗi trong exc.errors() =====
    for error in exc.errors():
        # --- Trích xuất thông tin từ error ---
        
        # error["loc"] là tuple/list chứa đường dẫn đến field bị lỗi
        # VD: ["body", "username"] → lỗi ở request body, field username
        # VD: ["query", "page"] → lỗi ở query params, field page
        # Ta lấy phần tử CUỐI CÙNG = tên field
        field_name = error["loc"][-1] if error["loc"] else "unknown"
        
        # error["type"] là loại lỗi (string_too_short, value_error, missing...)
        error_type = error["type"]
        
        # error["msg"] là message tiếng Anh gốc từ Pydantic
        original_msg = error["msg"]
        
        # error.get("ctx", {}) là context - chứa thông tin bổ sung
        # VD: {"min_length": 3, "max_length": 20}
        context = error.get("ctx", {})
        
        # error.get("input") là giá trị user đã nhập (dùng để debug)
        user_input = error.get("input")
        
        
        # ===== BƯỚC 3: Tìm message tiếng Việt tương ứng =====
        
        # Bước 3.1: Kiểm tra có template message cho error_type + field_name không
        message_template = VALIDATION_MESSAGES.get(error_type, {}).get(field_name)
        
        if message_template:
            # Bước 3.2: Nếu có template → thay thế {placeholder} bằng giá trị từ context
            # VD: "Tên đăng nhập phải có ít nhất {min_length} ký tự"
            #     + context = {"min_length": 3}
            #     → "Tên đăng nhập phải có ít nhất 3 ký tự"
            try:
                final_message = message_template.format(**context)
            except KeyError:
                # Nếu template có {placeholder} nhưng không có trong context
                # → Giữ nguyên template (fallback)
                final_message = message_template
        
        elif error_type == "value_error":
            # Bước 3.3: Trường hợp đặc biệt - value_error từ custom validator
            # Message đã là tiếng Việt từ validator (VD: raise ValueError("Lỗi..."))
            # Pydantic format thành: "Value error, {message}"
            # Ta LOẠI BỎ prefix "Value error, " để chỉ giữ message gốc
            final_message = original_msg.replace("Value error, ", "")
        
        else:
            # Bước 3.4: Không tìm thấy mapping → giữ nguyên message tiếng Anh
            # (Fallback để tránh crash, nên log ra để bổ sung sau)
            final_message = original_msg
            # TODO: Log warning để dev biết cần thêm mapping
            # logging.warning(f"Missing translation for {error_type}.{field_name}")
        
        
        # ===== BƯỚC 4: Thêm error đã format vào mảng kết quả =====
        translated_errors.append({
            "field": field_name,           # Tên field bị lỗi
            "message": final_message,      # Message tiếng Việt
            "type": error_type,            # Loại lỗi (để FE có thể xử lý đặc biệt nếu cần)
            # "input": user_input          # Uncomment nếu muốn debug (không nên trả về production)
        })
    
    
    # ===== BƯỚC 5: Trả về JSONResponse với errors đã dịch =====
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,  # 422 = Validation Error
        content={
            "detail": "Dữ liệu không hợp lệ",  # Message chung
            "errors": translated_errors         # Danh sách lỗi chi tiết
        }
    )


# ============================================================================
# HƯỚNG DẪN SỬ DỤNG:
# ============================================================================
# Trong file main.py, thêm dòng sau để đăng ký exception handler:
#
#   from fastapi.exceptions import RequestValidationError
#   from app.core.exceptions import validation_exception_handler
#
#   app.add_exception_handler(RequestValidationError, validation_exception_handler)
#
# Sau đó MỌI endpoint trong API sẽ tự động dùng handler này khi có lỗi validation.
# ============================================================================


# ============================================================================
# RESPONSE FORMAT MẪU:
# ============================================================================
# Khi user gửi request sai, API sẽ trả về:
#
# Status Code: 422
# Body:
# {
#   "detail": "Dữ liệu không hợp lệ",
#   "errors": [
#     {
#       "field": "username",
#       "message": "Tên đăng nhập phải có ít nhất 3 ký tự",
#       "type": "string_too_short"
#     },
#     {
#       "field": "email",
#       "message": "Email không hợp lệ. Vui lòng nhập đúng định dạng email",
#       "type": "value_error.email"
#     }
#   ]
# }
#
# Frontend chỉ cần loop qua errors[] và hiển thị message cho từng field.
# ============================================================================
