from flask import Blueprint

bp_files = Blueprint("files", __file__, url_prefix="/files")

from website_workshop.files import files
