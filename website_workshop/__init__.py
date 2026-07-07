from datetime import date, datetime
import os
from sqlite3 import connect
from flask import Flask
from pathlib import Path
from website_workshop.main import bp_main
from website_workshop.sql import bp_sql
from website_workshop.shell import bp_shell
from website_workshop.files import bp_files
from website_workshop.util.config import Config
from website_workshop.util.db import get_db
from website_workshop.combo import bp_combo


def create_app():
    app = Flask(__name__)

    app = register_blueprints(app)

    app.secret_key = os.urandom(24)

    with app.app_context():
        populate_db()

    app.config.from_object(Config)

    return app


def register_blueprints(app):
    app.register_blueprint(bp_main)
    app.register_blueprint(bp_sql)
    app.register_blueprint(bp_shell)
    app.register_blueprint(bp_files)
    app.register_blueprint(bp_combo)
    return app


def populate_db():
    db = get_db()

    r = db.execute("SELECT * FROM users;").fetchall()

    if len(r) > 0:
        return

    mock_users = [
        ("admin", datetime.now().isoformat()),
        ("guest", datetime.now().isoformat()),
        ("Arjan Draisma", datetime.now().isoformat()),
        ("Santa Clause", datetime.now().isoformat()),
    ]

    db.executemany(
        "INSERT OR IGNORE INTO users (name, created_at) VALUES (?, ?);", mock_users
    )

    db.commit()
