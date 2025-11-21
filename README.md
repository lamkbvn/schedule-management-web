# Ứng dụng Quản lý Lịch trình Cá nhân – Tích hợp AI xử lý Tiếng Việt tự nhiên

**Tên đồ án:** Xây dựng ứng dụng Quản lý Lịch trình Cá nhân tích hợp xử lý Tiếng Việt bằng Google Gemini AI  
**Tác giả:** [Mai Phúc Lâm ]  
**Năm thực hiện:** 12/2025  

Một trợ lý lịch trình thông minh dành riêng cho người Việt – chỉ cần nói một câu như:  
“Hẹn ny 7h tối nay xem phim, nhắc trước 30 phút” → hệ thống tự động tạo lịch hoàn chỉnh!

## Tính năng nổi bật
- Nhập lịch bằng tiếng Việt tự nhiên (có dấu, không dấu, viết tắt, nói chuyện đời thường)
- Tự động trích xuất: tên sự kiện, thời gian, địa điểm, nhắc nhở
- Giao diện web đẹp, responsive (dùng Flask + HTML/CSS/JS)
- Quản lý sự kiện: thêm, sửa, xóa, tìm kiếm, lọc theo ngày
- Lưu trữ cục bộ bằng SQLite
- Hệ thống nhắc nhở pop-up
- Hoàn toàn chạy offline (chỉ cần API key Gemini để dùng AI)

## Demo nhanh
![Demo](demo.gif) *(sẽ thêm sau khi có ảnh/video)*

## Yêu cầu hệ thống
- Python 3.11 (khuyến nghị dùng đúng phiên bản để tránh lỗi thư viện)
- Kết nối Internet (chỉ để gọi Google Gemini AI)

## Hướng dẫn cài đặt & chạy ứng dụng

### Bước 1: Clone source code
```bash
git clone https://github.com/lamkbvn/schedule-management-web.git
cd schedule-management-web
```

### Bước 2: Tạo và kích hoạt virtual environment (khuyến khích)
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### Bước 3: Cài đặt thư viện cần thiết
```bash
pip install -r requirements.txt
```

### Bước 4: Tạo API Key Google Gemini
1. Truy cập: https://aistudio.google.com/api-keys
2. Nhấn “Create API Key” → Copy key
3. Mở file `config.py` trong thư mục dự án
4. Dán key vào dòng:
   ```python
   api_key = "AIzaSy..._your_key_here_..."
   ```

### Bước 5: Khởi chạy ứng dụng
```bash
python app.py
```

Hoặc dùng lệnh ngắn gọn trên Windows:
```bash
py app.py
```

→ Ứng dụng sẽ tự động mở trình duyệt tại: http://127.0.0.1:5000

## Cách sử dụng
1. Mở trình duyệt → truy cập địa chỉ trên
2. Nhấn nút “Chat với AI” ở góc dưới
3. Gõ bất kỳ câu nào bằng tiếng Việt, ví dụ:
   - “Họp team 9h sáng mai phòng 301, nhắc trước 15 phút”
   - “hẹn cafe vs crush 6h30 chiều mai ở Highlands”
   - “đi gym tối nay 7h California”
4. Nhấn Enter → AI sẽ tự tạo lịch và thông báo thành công!

## Cấu trúc thư mục
```
schedule-management-web/
├── app.py                  # File chạy chính
├── config.py               # Chứa API key Gemini
├── requirements.txt        # Danh sách thư viện
├── database.db             # Tự động tạo khi chạy lần đầu
├── templates/              # HTML giao diện
├── static/                 # CSS, JS, hình ảnh
└── models.py, routes.py    # Xử lý backend
```

## Các lệnh hữu ích
```bash
# Xem phiên bản Python
python --version

# Cập nhật pip (nếu cần)
python -m pip install --upgrade pip

# Chạy lại sau khi sửa code
python app.py
``

## Tác giả & Liên hệ
- GitHub: [@lamkbvn](https://github.com/lamkbvn)
- Email: [lamkbvn@gmail.com]

> “Chỉ cần nói một câu tiếng Việt – lịch của bạn đã được sắp xếp gọn gàng!”
