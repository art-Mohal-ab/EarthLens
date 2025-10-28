import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "myecretkey"
    SQLALCHEMY_DATABASE_URI = os.environ.get("") or "sqlite:///earthlens.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
