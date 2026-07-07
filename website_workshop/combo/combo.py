from flask import render_template

from website_workshop.combo import bp_combo


@bp_combo.route("/", methods=["GET"])
def part1():
    return render_template("/combo/part1.html")
