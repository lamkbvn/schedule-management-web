# utils.py
from datetime import datetime
import pytz

VN_TZ = pytz.timezone('Asia/Ho_Chi_Minh')

def format_time(iso_string):
    """Chuyển ISO string → định dạng đẹp: 16/11/2025, 21:08"""
    try:
        dt = datetime.fromisoformat(iso_string)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=VN_TZ)
        return dt.strftime('%d/%m/%Y, %H:%M')
    except:
        return iso_string

def format_event_time(start_iso, end_iso):
    """Định dạng thời gian: 14:30 - 16:00"""
    try:
        start = datetime.fromisoformat(start_iso)
        if end_iso :
            end = datetime.fromisoformat(end_iso)
        else : end =  "--"
        return f"{start.strftime('%H:%M')} - {end.strftime('%H:%M') if end_iso else end}"
    except:
        return "Không xác định"

def format_event_date(iso_string):
    """Chỉ lấy ngày: 16/11/2025"""
    try:
        dt = datetime.fromisoformat(iso_string)
        return dt.strftime('%d/%m/%Y')
    except:
        return "Không xác định"

def is_event_completed(event, now=None):
    """
    Xác định sự kiện đã hoàn thành chưa.
    Ưu tiên: Nếu người dùng đã đánh dấu thủ công (isComplete = 1) → trả về True
    Nếu chưa đánh dấu → mới tự động kiểm tra theo end_time
    """
    if now is None:
        now = datetime.now(VN_TZ)

    # 1. Ưu tiên trạng thái người dùng đánh dấu thủ công
    if event.get('isComplete', 0) == 1:
        return True

    # 2. Nếu không có end_time → chưa thể coi là hoàn thành (vì chưa kết thúc)
    if not event.get('end_time'):
        return False

    # 3. Kiểm tra end_time có hợp lệ và đã qua chưa
    try:
        end_time_dt = datetime.fromisoformat(event['end_time'])
        # Nếu end_time không có timezone → giả định là giờ Việt Nam
        if end_time_dt.tzinfo is None:
            end_time_dt = VN_TZ.localize(end_time_dt)
        return end_time_dt < now
    except (ValueError, TypeError):
        # Nếu end_time bị lỗi định dạng → không coi là hoàn thành
        return False