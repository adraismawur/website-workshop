from flask import Blueprint

bp_main = Blueprint("main", __file__)

from website_workshop.main import main
