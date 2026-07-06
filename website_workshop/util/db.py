
from pathlib import Path
from sqlite3 import connect

from flask import g

from website_workshop.util.config import Config


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