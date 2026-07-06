from flask import render_template

from website_workshop.files import bp_files

@bp_files.route("/", methods=["GET"])
def part1():
    return render_template(
        "/files/part1.html"
    )
