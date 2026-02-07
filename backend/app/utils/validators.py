"""
Validators - Các hàm validate dữ liệu custom.

Dùng để kiểm tra tính hợp lệ của dữ liệu trước khi lưu vào database.
"""

import re


def validate_username(username: str) -> str:
    """
    Validate và chuẩn hóa username.
    
    Args:
        username: Username cần validate
        
    Returns:
        str: Username đã chuẩn hóa (stripped)
        
    Raises:
        ValueError: Nếu username không hợp lệ
        
    Yêu cầu:
        - Chỉ chứa chữ cái (a-z, A-Z), số (0-9), và gạch dưới (_)
        - Tự động loại bỏ khoảng trắng đầu/cuối
    """
    # Loại bỏ whitespace đầu cuối
    username = username.strip()
    
    # Check pattern: chỉ cho phép a-z, A-Z, 0-9, underscore
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        raise ValueError('Username chỉ chứa chữ cái, số và gạch dưới (_)')
    
    return username


def validate_full_name(full_name: str) -> str:
    """
    Validate và chuẩn hóa họ tên.
    
    Args:
        full_name: Họ tên cần validate
        
    Returns:
        str: Họ tên đã chuẩn hóa
        
    Raises:
        ValueError: Nếu họ tên không hợp lệ
        
    Xử lý:
        - Loại bỏ khoảng trắng đầu/cuối
        - Chuẩn hóa nhiều khoảng trắng liên tiếp thành 1
        - Không cho phép tên rỗng
    """
    # Loại bỏ whitespace đầu cuối
    full_name = full_name.strip()
    
    # Check không được rỗng
    if not full_name:
        raise ValueError('Họ tên không được để trống')
    
    # Loại bỏ nhiều khoảng trắng liên tiếp thành 1
    full_name = re.sub(r'\s+', ' ', full_name)
    
    return full_name


def validate_password_strength(password: str) -> str:
    """
    Validate độ mạnh của mật khẩu.
    
    Args:
        password: Mật khẩu cần kiểm tra
        
    Returns:
        str: Password nếu hợp lệ
        
    Raises:
        ValueError: Nếu password không đủ mạnh với thông báo cụ thể
        
    Yêu cầu:
        - Ít nhất 6 ký tự
        - Có ít nhất 1 chữ hoa
        - Có ít nhất 1 chữ thường
        - Có ít nhất 1 số
        - Có ít nhất 1 ký tự đặc biệt
    """
    # Validate độ dài tối thiểu
    if len(password) < 6:
        raise ValueError('Mật khẩu phải có ít nhất 6 ký tự')
    
    # Validate có chữ hoa
    if not re.search(r'[A-Z]', password):
        raise ValueError('Mật khẩu phải có ít nhất 1 chữ hoa')
    
    # Validate có chữ thường
    if not re.search(r'[a-z]', password):
        raise ValueError('Mật khẩu phải có ít nhất 1 chữ thường')
    
    # Validate có số
    if not re.search(r'[0-9]', password):
        raise ValueError('Mật khẩu phải có ít nhất 1 số')
    
    # Validate có ký tự đặc biệt
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        raise ValueError('Mật khẩu phải có ít nhất 1 ký tự đặc biệt (!@#$%^&*...)')
    
    return password


def validate_frequency_array(frequency: list[int]) -> bool:
    """
    Kiểm tra mảng frequency hợp lệ.
    
    Args:
        frequency: Mảng các số đại diện cho thứ trong tuần
        
    Returns:
        bool: True nếu tất cả phần tử trong khoảng 0-6
        
    Quy ước:
        - 0 = Thứ 2 (Monday)
        - 1 = Thứ 3 (Tuesday)
        - ...
        - 6 = Chủ nhật (Sunday)
    """
    pass


def validate_color_hex(color: str) -> bool:
    """
    Kiểm tra mã màu hex hợp lệ.
    
    Args:
        color: Mã màu hex (VD: "#FF5733")
        
    Returns:
        bool: True nếu format đúng #RRGGBB
        
    Format: #RRGGBB (# theo sau bởi 6 ký tự hex)
    """
    pass


def validate_phone_vietnam(phone: str) -> bool:
    """
    Kiểm tra số điện thoại Việt Nam hợp lệ.
    
    Args:
        phone: Số điện thoại cần kiểm tra
        
    Returns:
        bool: True nếu số điện thoại hợp lệ
        
    Format: 
        - 0xxxxxxxxx (10 số, bắt đầu bằng 0)
        - +84xxxxxxxxx (12 số, bắt đầu bằng +84)
        - Đầu số: 03, 05, 07, 08, 09
    """
    pass


def validate_email_format(email: str) -> bool:
    """
    Kiểm tra format email hợp lệ.
    
    Args:
        email: Email cần kiểm tra
        
    Returns:
        bool: True nếu format email hợp lệ
        
    Dùng regex để kiểm tra format cơ bản của email.
    """
    pass

def check_password(pw_plain: str, pw_hashed: str ) -> str: 
    pass
