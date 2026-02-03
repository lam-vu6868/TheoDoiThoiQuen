"""
Notifications - Các hàm gửi thông báo (Optional - cần service bên ngoài).

Dùng để gửi push notification, SMS, in-app notification...
Cần cài thêm: firebase-admin, twilio, hoặc OneSignal
"""

from datetime import datetime


def send_push_notification(user_id: int, title: str, message: str, data: dict = None) -> bool:
    """
    Gửi push notification đến device của user.
    
    Args:
        user_id: ID của user
        title: Tiêu đề notification
        message: Nội dung notification
        data: Dict chứa dữ liệu thêm (optional)
        
    Returns:
        bool: True nếu gửi thành công
        
    Cần:
        - Firebase Cloud Messaging (FCM)
        - Hoặc OneSignal
        - Device token của user (lưu trong database)
    """
    pass


def schedule_habit_reminder(user_id: int, habit_id: int, reminder_time: datetime) -> bool:
    """
    Lên lịch nhắc nhở habit vào thời gian cụ thể.
    
    Args:
        user_id: ID của user
        habit_id: ID của habit
        reminder_time: Thời gian nhắc nhở
        
    Returns:
        bool: True nếu lên lịch thành công
        
    Cần:
        - Celery + Redis (background tasks)
        - Hoặc APScheduler
        - Lưu schedule vào database
    """
    pass


def send_streak_notification(user_id: int, habit_name: str, streak_days: int) -> bool:
    """
    Gửi notification khi đạt milestone streak.
    
    Args:
        user_id: ID của user
        habit_name: Tên habit
        streak_days: Số ngày streak
        
    Returns:
        bool: True nếu gửi thành công
        
    Chỉ gửi khi đạt milestone: 7, 30, 100, 365 ngày
    """
    pass


def send_daily_reminder(user_id: int, pending_habits: list) -> bool:
    """
    Gửi nhắc nhở tổng hợp các habits chưa làm trong ngày.
    
    Args:
        user_id: ID của user
        pending_habits: List các habit chưa check-in
        
    Returns:
        bool: True nếu gửi thành công
        
    Gửi vào cuối ngày (VD: 9 PM) để nhắc user check-in.
    """
    pass


def send_sms_notification(phone: str, message: str) -> bool:
    """
    Gửi SMS notification (Optional - tốn phí).
    
    Args:
        phone: Số điện thoại
        message: Nội dung SMS (tối đa 160 ký tự)
        
    Returns:
        bool: True nếu gửi thành công
        
    Cần:
        - Twilio API
        - Hoặc VNPT SMS
        - API key và tài khoản
    """
    pass


def create_in_app_notification(user_id: int, title: str, message: str, notification_type: str) -> dict:
    """
    Tạo notification trong app (lưu vào database).
    
    Args:
        user_id: ID của user
        title: Tiêu đề
        message: Nội dung
        notification_type: Loại notification ("achievement", "reminder", "info")
        
    Returns:
        dict: Thông tin notification vừa tạo
        
    Notification này được lưu trong database và hiển thị trong app.
    User có thể đánh dấu đã đọc hoặc xóa.
    """
    pass
