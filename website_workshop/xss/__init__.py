from flask import Blueprint

bp_xss = Blueprint("xss", __file__, url_prefix="/xss")

from website_workshop.xss import xss
