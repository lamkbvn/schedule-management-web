import datetime
import json
from config import Config
from google import genai

# Tạo client Gemini
client = genai.Client(api_key=Config.api_key)

# ---------------- TẠO CHAT SESSION ----------------
chat_session = client.chats.create(model="gemini-2.5-flash")

# ---------------- BASE PROMPT GỬI 1 LẦN ----------------
time_current = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

BASE_PROMPT = f"""
Bạn là hệ thống phân tích tiếng Việt để trích thông tin lập lịch.

Thời gian hiện tại: {time_current}

Luôn xuất kết quả JSON:
{{
  "event": string hoặc null,
  "start_time": YYYY-MM-DDTHH:MM hoặc null,
  "end_time": YYYY-MM-DDTHH:MM hoặc null,
  "location": string hoặc null,
  "reminder_minutes": number hoặc 0
}}

Quy tắc:
- Không ước lượng thời gian
- Không đoán thời gian nếu không có trong câu
- Dùng giờ 24h
- Không thêm giải thích
- Không markdown
- Chỉ trả về JSON thuần
"""

# Gửi base prompt 1 lần
chat_session.send_message(BASE_PROMPT)

print("hello")
# ------------------- HÀM GỌI GEMINI -------------------
def ask_gemini(user_input: str):
    response = chat_session.send_message(user_input)
    text = response.text
    print(text)
    return json.loads(text)

def test_ask_gemini(user_input: str):
    response = chat_session.send_message(user_input)
    text = response.text
    return text


# testcase = [
#     "Nhắc tôi tham dự lễ trao giải bắt đầu lúc 19h tối thứ 6 tuần này tại Nhà hát Thành phố",
# ]
#
# for t in testcase  :
#     r = test_ask_gemini(t)
#     print(r)





































###########################################################################################################################
# import datetime
# import json
# from idlelib.debugger_r import restart_subprocess_debugger
# from config import  Config
#
# from google import genai
#
# client = genai.Client(api_key=Config.api_key)
#
# def ask_gemini(prompt: str):
#     # Lấy thời gian hiện tại
#     time_current = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#
#     # Prompt mặc định — luôn có thời gian + hướng dẫn định dạng JSON
#     full_prompt = f"""
# Thời gian hiện tại: {time_current}
#
# Hãy đọc yêu cầu bên dưới và xuất kết quả với các trường:
# {{
#   "event": string hoặc null nếu không tìm thấy thông tin về tên sự kiên,
#   "start_time": YYYY-MM-DDTHH:MM hoặc null nếu không tìm thấy thông tin về  thời gian , không được tự ước lượng thời gian  ,
#   "end_time": YYYY-MM-DDTHH:MM hoặc null nếu không tìm thấy thông tin về  thời gian , không được tự ước lượng thời gian ,
#   "location": string ,
#   "reminder_minutes": number hoặc 0 nếu không có
# }}
#
# Chỉ trả về kết quả ,  không được đoán mò , sử dụng thời gian 24 giờ , không thêm giải thích ,Không thêm json hoặc ký tự Markdown .
#
# Yêu cầu: {prompt}
# """
#
#     # Gọi Gemini
#     response = client.models.generate_content(
#         model="gemini-2.5-flash",
#         contents=full_prompt,
#     )
#     print(response.text)
#     data = json.loads(response.text)
#     return data

# result = ask_gemini("Họp team vào 9h sáng ngày mai tại phòng họp A, nhắc trước 15 phút")
# #
# # if not result["event"]:
# #     print("Chào bạn 👋 Tôi là AI chuyên giúp quản lý và sắp xếp lịch trình.")
# #     print("Bạn có thể nói như: 'Nhắc tôi họp nhóm lúc 9 giờ sáng mai'.")
# # else:
# #     print("ban da tao lich trinh thanh cong")
#
#
# testcase = [
#     "Họp team vào 9h sáng ngày mai tại phòng họp A, nhắc trước 15 phút",
#     "Hội thảo từ 8h đến 17h ngày 25/12/2024 tại Trung tâm Hội nghị",
#     "Sinh nhật bạn An lúc 18h30 đến 21h thứ 7 tuần sau tại nhà hàng"
#     "Meeting với client lúc 14h chiều mai 2 tiếng qua Zoom",
#     "Du lịch từ 7h sáng 01/01/2025 đến 19h tối 03/01/2025"
# ]