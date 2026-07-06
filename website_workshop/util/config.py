import os


class Config:
    DB_PATH = os.environ.get("DB_PATH", "./secure-web.db")
    SECRET_KEY = os.environ.get("SECRET_KEY", "CHANGEME")
