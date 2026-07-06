import os
from sqlite3 import connect
from flask import Flask, g
from pathlib import Path
from website_workshop.main import bp_main


def create_app():
    app = Flask(__name__)

    app = register_blueprints(app)


    class Config:
        DB_PATH = os.environ.get("DB_PATH", "./secure-web.db")


    app.config.from_object(Config)

    return app


def get_db():
    if "db" not in g:
        db = connect(Config.DB_PATH)

        p = Path(__file__).parent

        print(p)

        with open(p / "db_schema.sql", "r") as schema:
            schema = schema.read()
            print(schema)
            db.cursor().executescript(schema)
            db.commit()

        g.db = db

    return g.db

def register_blueprints(app):
    app.register_blueprint(bp_main)
    return app
