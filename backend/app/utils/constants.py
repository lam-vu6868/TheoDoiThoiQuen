"""
Constants - Các hằng số dùng chung trong toàn bộ app.

Tập trung tất cả magic strings và magic numbers vào một chỗ.
"""

# ==================== HABIT STATUS ====================
# Trạng thái của một habit log
HABIT_STATUS_COMPLETED = "COMPLETED"  # Đã hoàn thành
HABIT_STATUS_SKIPPED = "SKIPPED"      # Bỏ qua (có lý do)
HABIT_STATUS_FAILED = "FAILED"        # Không hoàn thành

# List tất cả status hợp lệ
VALID_HABIT_STATUSES = [
    HABIT_STATUS_COMPLETED,
    HABIT_STATUS_SKIPPED,
    HABIT_STATUS_FAILED,
]


# ==================== USER ROLES ====================
# Vai trò của user
ROLE_ADMIN = "admin"  # Quản trị viên - full quyền
ROLE_USER = "user"    # User thường - chỉ quản lý habits của mình

# List tất cả roles hợp lệ
VALID_ROLES = [ROLE_ADMIN, ROLE_USER]


# ==================== WEEKDAYS ====================
# Map số ngày sang tên tiếng Việt
# 0 = Monday, 6 = Sunday (theo Python datetime)
WEEKDAYS = {
    0: "Thứ 2",
    1: "Thứ 3",
    2: "Thứ 4",
    3: "Thứ 5",
    4: "Thứ 6",
    5: "Thứ 7",
    6: "Chủ nhật",
}


# ==================== DEFAULT COLORS ====================
# Màu mặc định cho habits (HEX colors)
DEFAULT_COLORS = [
    "#FF5733",  # Đỏ cam
    "#33FF57",  # Xanh lá
    "#3357FF",  # Xanh dương
    "#F333FF",  # Tím hồng
    "#FFC300",  # Vàng
    "#FF33A8",  # Hồng
    "#33FFF0",  # Cyan
    "#FF8C33",  # Cam
]


# ==================== PAGINATION ====================
# Cấu hình phân trang
DEFAULT_PAGE_SIZE = 20      # Số items mặc định mỗi trang
MAX_PAGE_SIZE = 100         # Số items tối đa mỗi trang
MIN_PAGE_SIZE = 1           # Số items tối thiểu


# ==================== TOKEN & AUTHENTICATION ====================
# Thời gian hết hạn token (phút)
ACCESS_TOKEN_EXPIRE_MINUTES = 1440    # 1 ngày (24 * 60)
REFRESH_TOKEN_EXPIRE_DAYS = 30        # 30 ngày


# ==================== HABIT LIMITS ====================
# Giới hạn cho habits
MAX_HABITS_PER_USER = 50              # User thường tối đa 50 habits
MAX_HABITS_PER_USER_ADMIN = 999       # Admin không giới hạn
MAX_HABIT_NAME_LENGTH = 100           # Tên habit tối đa 100 ký tự
MAX_HABIT_DESC_LENGTH = 500           # Mô tả tối đa 500 ký tự


# ==================== STREAK MILESTONES ====================
# Các mốc streak đặc biệt (để gửi notification chúc mừng)
STREAK_MILESTONES = [7, 14, 30, 60, 100, 365]


# ==================== DATE FORMATS ====================
# Format ngày tháng chuẩn
DATE_FORMAT = "%Y-%m-%d"              # 2026-02-03
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S" # 2026-02-03 14:30:00
DISPLAY_DATE_FORMAT = "%d/%m/%Y"      # 03/02/2026 (kiểu Việt Nam)


# ==================== ERROR MESSAGES ====================
# Các thông báo lỗi chuẩn
ERROR_USER_NOT_FOUND = "User không tồn tại"
ERROR_HABIT_NOT_FOUND = "Habit không tồn tại"
ERROR_INVALID_CREDENTIALS = "Email hoặc mật khẩu không đúng"
ERROR_EMAIL_ALREADY_EXISTS = "Email đã được sử dụng"
ERROR_USERNAME_ALREADY_EXISTS = "Username đã được sử dụng"
ERROR_PERMISSION_DENIED = "Bạn không có quyền thực hiện thao tác này"
ERROR_INVALID_TOKEN = "Token không hợp lệ hoặc đã hết hạn"
