"""
Email - Các hàm gửi email (Optional - cần cấu hình SMTP).

Dùng để gửi email thông báo, reset password, welcome email...
Cần cài thêm: fastapi-mail hoặc sendgrid
"""


def send_welcome_email(email: str, username: str) -> bool:
    """
    Gửi email chào mừng khi user đăng ký mới.
    
    Args:
        email: Email của user
        username: Username của user
        
    Returns:
        bool: True nếu gửi thành công
        
    Nội dung email:
        - Chào mừng user
        - Hướng dẫn bắt đầu sử dụng app
        - Link tới trang chính
    """
    pass


def send_password_reset_email(email: str, reset_token: str) -> bool:
    """
    Gửi email reset mật khẩu.
    
    Args:
        email: Email của user
        reset_token: Token để reset password (JWT)
        
    Returns:
        bool: True nếu gửi thành công
        
    Nội dung email:
        - Link reset password (có chứa token)
        - Thời gian hết hạn của link (VD: 15 phút)
        - Cảnh báo nếu không phải họ yêu cầu
    """
    pass


def send_habit_reminder_email(email: str, habit_name: str, scheduled_time: str) -> bool:
    """
    Gửi email nhắc nhở làm habit.
    
    Args:
        email: Email của user
        habit_name: Tên habit cần nhắc
        scheduled_time: Thời gian dự định làm
        
    Returns:
        bool: True nếu gửi thành công
        
    Nội dung email:
        - Nhắc nhở về habit
        - Thời gian nên làm
        - Link quick check-in
    """
    pass


def send_streak_achievement_email(email: str, username: str, streak_days: int, habit_name: str) -> bool:
    """
    Gửi email chúc mừng đạt milestone streak.
    
    Args:
        email: Email của user
        username: Username
        streak_days: Số ngày streak (7, 30, 100, 365...)
        habit_name: Tên habit
        
    Returns:
        bool: True nếu gửi thành công
        
    Nội dung email:
        - Chúc mừng milestone
        - Động viên tiếp tục
        - Hiển thị badge/achievement
    """
    pass


def send_weekly_report_email(email: str, username: str, report_data: dict) -> bool:
    """
    Gửi email báo cáo tuần.
    
    Args:
        email: Email của user
        username: Username
        report_data: Dict chứa dữ liệu báo cáo
            {
                "total_habits": 5,
                "completed_this_week": 28,
                "best_streak": 14,
                "completion_rate": 80.0
            }
        
    Returns:
        bool: True nếu gửi thành công
        
    Nội dung email:
        - Tổng quan tuần qua
        - Habits hoàn thành tốt nhất
        - Habits cần cải thiện
        - Motivational quote
    """
    pass
