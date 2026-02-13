"""app.utils.email
Hàm gửi email cơ bản sử dụng Python built-in `smtplib`.

Hàm dùng `asyncio.to_thread` để thực thi phần gửi mail blocking trong threadpool
và vẫn giữ interface `async def` để có thể `await` từ các endpoint.

Yêu cầu: cấu hình SMTP trong `backend/.env` (đã load vào `app.core.config.settings`):
 - MAIL_SERVER, MAIL_PORT, MAIL_USERNAME, MAIL_PASSWORD, MAIL_FROM, MAIL_FROM_NAME
 - MAIL_STARTTLS (bool), MAIL_SSL_TLS (bool)
"""

import asyncio
import smtplib
from email.message import EmailMessage
from typing import Optional
from app.core.config import settings


def _build_message(subject: str, to_email: str, body: str, subtype: str = "plain") -> EmailMessage:
    msg = EmailMessage()
    msg["From"] = f"{settings.MAIL_FROM_NAME or ''} <{settings.MAIL_FROM or settings.MAIL_USERNAME}>"
    msg["To"] = to_email
    msg["Subject"] = subject
    if subtype == "html":
        msg.add_alternative(body, subtype="html")
    else:
        msg.set_content(body)
    return msg


def _send_via_smtp(msg: EmailMessage) -> None:
    host = settings.MAIL_SERVER
    port = int(settings.MAIL_PORT or 0)
    username = settings.MAIL_USERNAME
    password = settings.MAIL_PASSWORD
    use_starttls = bool(settings.MAIL_STARTTLS)
    use_ssl = bool(settings.MAIL_SSL_TLS)

    if use_ssl:
        with smtplib.SMTP_SSL(host, port) as server:
            server.login(username, password)
            server.send_message(msg)
    else:
        with smtplib.SMTP(host, port) as server:
            server.ehlo()
            if use_starttls:
                server.starttls()
                server.ehlo()
            if username and password:
                server.login(username, password)
            server.send_message(msg)


async def send_welcome_email(email: str, username: str) -> bool:
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
    subject = "Welcome to Habit Tracker"
    body = (
        f"Xin chào {username},\n\n"
        "Chào mừng bạn đến với Habit Tracker! Bắt đầu tạo thói quen tốt ngay hôm nay.\n\n"
        "Trân trọng,\nTeam Habit Tracker"
    )
    msg = _build_message(subject, email, body, subtype="plain")
    try:
        await asyncio.to_thread(_send_via_smtp, msg)
        return True
    except Exception:
        return False


async def send_password_reset_email(email: str, reset_token: str) -> bool:
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
    # Build reset link (frontend should handle the route /reset-password)
    reset_link = f"{settings.FRONTEND_URL.rstrip('/')}" + f"/reset-password?token={reset_token}"
    subject = "[Habit Tracker] Đặt lại mật khẩu"
    html = (
        f"<p>Xin chào,</p>"
        f"<p>Bạn (hoặc ai đó) đã yêu cầu đặt lại mật khẩu cho tài khoản của bạn. "
        f"Vui lòng nhấn vào liên kết bên dưới để đặt mật khẩu mới. Liên kết sẽ hết hạn sau một khoảng thời gian ngắn.</p>"
        f"<p><a href=\"{reset_link}\">Đặt lại mật khẩu</a></p>"
        f"<p>Nếu bạn không yêu cầu điều này, hãy bỏ qua email này.</p>"
        f"<p>Trân trọng,<br/>Team Habit Tracker</p>"
    )
    msg = _build_message(subject, email, html, subtype="html")
    try:
        await asyncio.to_thread(_send_via_smtp, msg)
        return True
    except Exception:
        return False


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
    return False


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
    return False


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
    return False
