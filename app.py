# app.py
from flask import Flask
from routes import main_bp
from models import init_db
from config import Config


app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = Config.SECRET_KEY

app.register_blueprint(main_bp)

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)