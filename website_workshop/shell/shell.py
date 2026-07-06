from flask import render_template

from website_workshop.shell import bp_shell

@bp_shell.route("/", methods=["GET"])
def part1():
    return render_template(
        "/shell/part1.html"
    )
