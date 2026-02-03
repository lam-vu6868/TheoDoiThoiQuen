"""
Validators - Các hàm validate dữ liệu custom.

Dùng để kiểm tra tính hợp lệ của dữ liệu trước khi lưu vào database.
"""


def validate_password_strength(password: str) -> tuple[bool, str]:
    """
    Kiểm tra độ mạnh của mật khẩu.
    
    Args:
        password: Mật khẩu cần kiểm tra
        
    Returns:
        tuple: (is_valid, message)
        - is_valid: True nếu mật khẩu hợp lệ
        - message: Thông báo lỗi hoặc thành công
        
    Yêu cầu:
        - Ít nhất 8 ký tự
        - Có ít nhất 1 chữ hoa
        - Có ít nhất 1 chữ thường
        - Có ít nhất 1 số
        - (Optional) Có ít nhất 1 ký tự đặc biệt
    """
    pass


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
