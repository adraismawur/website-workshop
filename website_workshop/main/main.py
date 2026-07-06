from flask import render_template
from website_workshop.main import bp_main


@bp_main.route("/", methods=["GET"])
def index():
    return render_template("/main/index.html")

@bp_main.route("/", methods=["GET"])
def login():
    return render_template("/main/index.html")
    