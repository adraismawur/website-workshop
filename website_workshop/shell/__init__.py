from flask import Blueprint

bp_shell = Blueprint("shell", __file__, url_prefix="/shell")

from website_workshop.shell import shell
