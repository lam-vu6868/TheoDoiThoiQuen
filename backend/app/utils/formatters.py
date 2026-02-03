"""
Formatters - Các hàm format và tính toán dữ liệu.

Dùng để format dữ liệu trước khi hiển thị hoặc tính toán các metrics.
"""

from datetime import date, datetime


def format_vietnamese_date(date_obj: date) -> str:
    """
    Format ngày theo kiểu Việt Nam.
    
    Args:
        date_obj: Đối tượng date cần format
        
    Returns:
        str: "Thứ 2, 03/02/2026"
        
    Quy ước:
        - Thứ 2, Thứ 3, ..., Thứ 7, Chủ nhật
        - Ngày/Tháng/Năm
    """
    pass


def format_habit_value(value: float, unit: str) -> str:
    """
    Format giá trị habit với đơn vị.
    
    Args:
        value: Giá trị số (5.2, 30, 2.5)
        unit: Đơn vị ("km", "trang", "ly nước")
        
    Returns:
        str: "5.2 km", "30 trang", "2.5 ly nước"
        
    Làm tròn đến 1 chữ số thập phân.
    """
    pass


def calculate_streak(logs: list) -> int:
    """
    Tính streak - số ngày liên tục hoàn thành habit.
    
    Args:
        logs: Danh sách HabitLog objects, sorted theo record_date
        
    Returns:
        int: Số ngày streak hiện tại
        
    Logic:
        - Bắt đầu từ hôm nay
        - Đếm ngược các ngày liên tục có status = "COMPLETED"
        - Dừng khi gặp ngày không COMPLETED hoặc ngày bị skip
    """
    pass


def calculate_completion_rate(logs: list) -> float:
    """
    Tính tỷ lệ hoàn thành (%).
    
    Args:
        logs: Danh sách HabitLog objects
        
    Returns:
        float: Phần trăm hoàn thành (0.0 - 100.0)
        
    Logic:
        - Đếm số logs có status = "COMPLETED"
        - Chia cho tổng số logs
        - Nhân 100 để ra %
    """
    pass


def format_percentage(value: float) -> str:
    """
    Format số thành phần trăm.
    
    Args:
        value: Giá trị từ 0-100
        
    Returns:
        str: "85.5%"
        
    Làm tròn đến 1 chữ số thập phân.
    """
    pass


def get_week_range(date_obj: date) -> tuple[date, date]:
    """
    Lấy ngày đầu và cuối của tuần.
    
    Args:
        date_obj: Ngày bất kỳ trong tuần
        
    Returns:
        tuple: (start_date, end_date)
        - start_date: Thứ 2 của tuần
        - end_date: Chủ nhật của tuần
    """
    pass


def format_duration(seconds: int) -> str:
    """
    Format thời gian từ giây sang chuỗi dễ đọc.
    
    Args:
        seconds: Số giây
        
    Returns:
        str: "2 giờ 30 phút", "45 phút", "10 giây"
        
    Tự động chọn đơn vị phù hợp (giờ, phút, giây).
    """
    pass
