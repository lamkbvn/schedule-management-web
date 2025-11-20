import datetime
import json
from idlelib.debugger_r import restart_subprocess_debugger

from google import genai

client = genai.Client(api_key="AIzaSyCmbIlt2oLJLMRMXM_AiEVADRgDq2Mv8QU")

def ask_gemini(prompt: str):
    # Lấy thời gian hiện tại
    time_current = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Prompt mặc định — luôn có thời gian + hướng dẫn định dạng JSON
    full_prompt = f"""
Thời gian hiện tại: {time_current}

Hãy đọc yêu cầu bên dưới và xuất kết quả với các trường:
{{
  "event": string hoặc null nếu không tìm thấy thông tin về tên sự kiên,
  "start_time": YYYY-MM-DDTHH:MM hoặc null nếu không tìm thấy thông tin về  thời gian , không được tự ước lượng thời gian  ,
  "end_time": YYYY-MM-DDTHH:MM hoặc null nếu không tìm thấy thông tin về  thời gian , không được tự ước lượng thời gian ,
  "location": string ,
  "reminder_minutes": number hoặc 0 nếu không có
}}

Chỉ trả về kết quả ,  không được đoán mò , sử dụng thời gian 24 giờ , không thêm giải thích ,Không thêm json hoặc ký tự Markdown .

Yêu cầu: {prompt}
"""

    # Gọi Gemini
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=full_prompt,
    )
    print(response.text)
    data = json.loads(response.text)
    return data

result = ask_gemini("Hẹn cà phê với Minh thứ 7 ở Highlands")

if not result["event"]:
    print("Chào bạn 👋 Tôi là AI chuyên giúp quản lý và sắp xếp lịch trình.")
    print("Bạn có thể nói như: 'Nhắc tôi họp nhóm lúc 9 giờ sáng mai'.")
else:
    print("ban da tao lich trinh thanh cong")


