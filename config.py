# config.py
import secrets

class Config:
    SECRET_KEY = secrets.token_hex(16)
    DATABASE = 'events.db'
    api_key= "AIzaSyBTIWRa83RQvvJbk3QwXVsV-0aFFUbr0H0"