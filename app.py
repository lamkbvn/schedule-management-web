# app.py
import sys

from flask import Flask
from routes import main_bp
from models import init_db
from config import Config


app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = Config.SECRET_KEY

app.register_blueprint(main_bp)

# if __name__ == '__main__':
#     init_db()
#     app.run(debug=True, port=5000)
#

if __name__ == '__main__':
    init_db()

    import webbrowser
    import threading
    import time
    import os


    def open_browser():
        time.sleep(1.5)  # đợi chắc chắn server lên
        url = "http://127.0.0.1:5000"
        print(f"Đang mở trình duyệt: {url}")
        try:
            # Cách 1: Dùng hệ điều hành mở (chắc chắn hiện)
            if os.name == 'nt':  # Windows
                os.startfile(url)
            elif os.name == 'posix':  # macOS / Linux
                os.system(f"open {url}" if sys.platform == "darwin" else f"xdg-open {url}")
        except:
            # Cách 2: fallback về webbrowser
            webbrowser.open_new_tab(url)


    # Tạo thread riêng để mở trình duyệt
    threading.Thread(target=open_browser, daemon=True).start()

    # Khởi động Flask
    app.run(debug=True, port=5000, use_reloader=False)
    # Quan trọng: thêm use_reloader=False để tránh chạy 2 lần!