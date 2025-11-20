# config.py
import secrets

class Config:
    SECRET_KEY = secrets.token_hex(16)
    DATABASE = 'events.db'