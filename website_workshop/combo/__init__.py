from flask import Blueprint

bp_combo = Blueprint("combo", __file__, url_prefix="/combo")

from website_workshop.combo import combo
