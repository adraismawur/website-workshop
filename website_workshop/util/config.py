import os
from pathlib import Path


class Config:
    DB_PATH = os.environ.get("DB_PATH", "./secure-web.db")
    SECRET_KEY = os.environ.get("SECRET_KEY", "CHANGEME")
    UPLOAD_FOLDER = (
        Path(os.environ.get("UPLOAD_FOLDER", "./uploads")).expanduser().absolute()
    )
