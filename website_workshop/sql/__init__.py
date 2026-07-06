from flask import Blueprint

bp_sql = Blueprint("sql", __file__, url_prefix="/sql")

from website_workshop.sql import sql
