from flask import render_template

from website_workshop.xss import bp_xss

@bp_xss.route("/", methods=["GET"])
def part1():
    return render_template(
        "/xss/part1.html"
    )
