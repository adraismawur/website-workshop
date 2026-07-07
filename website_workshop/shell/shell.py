from flask import flash, make_response, render_template, request
from subprocess import run, STDOUT
from shlex import quote

from wtforms import Form, SelectField, StringField, SubmitField

from website_workshop.shell import bp_shell


class FormatForm(Form):
    formatting = StringField()
    submit = SubmitField("Show date", render_kw={"class": "btn"})


class ProgramForm(Form):
    program = SelectField(
        choices=[
            "date",
            "uptime",
        ],
    )
    submit = SubmitField("Run", render_kw={"class": "btn"})


def call_program_safe(program: str):
    out = run(program, capture_output=True)

    if out.returncode != 0:
        output = out.stderr.decode("utf-8")
        raise RuntimeError(
            f"Failed to run {program} command: {output}"
        )

    return out.stdout.decode("utf-8")


def call_date_unsafe(formatting: str = None):
    command = "date"

    if formatting:
        if not formatting.startswith("+"):
            formatting = "+" + formatting
        command = command + " " + formatting

    out = run(command, capture_output=True, shell=True)

    if out.returncode != 0:
        raise RuntimeError("Failed to run date command: " + out.stderr.decode("utf-8"))

    return out.stdout.decode("utf-8")


def call_date_safe(formatting: str = None):
    args = ["date"]

    if formatting:
        if not formatting.startswith("+"):
            formatting = "+" + formatting
        args.append(quote(formatting))

    out = run(args, capture_output=True)

    if out.returncode != 0:
        raise RuntimeError("Failed to run date command: " + out.stderr.decode("utf-8"))

    return out.stdout.decode("utf-8")


@bp_shell.route("/1", methods=["GET", "POST"])
def part1():
    plain_date_output = call_date_safe()

    form = FormatForm(request.form)

    formatted_date_output = None
    formatted_date_error = None
    formatting = None

    if request.method == "POST":
        formatting = form.formatting.data
        if not formatting.startswith("+") and not formatting == "":
            formatting = "+" + formatting
        if not formatting == "":
            formatting = quote(formatting)

        try:
            formatted_date_output = call_date_safe(form.formatting.data)
        except RuntimeError as e:
            formatted_date_error = e

    return render_template(
        "/shell/part1.html",
        plain_date_output=plain_date_output,
        form=form,
        formatted_date_output=formatted_date_output,
        formatted_date_error=formatted_date_error,
        formatting=formatting,
    )


@bp_shell.route("/2", methods=["GET", "POST"])
def part2():
    plain_date_output = call_date_safe()

    form = FormatForm(request.form)

    formatted_date_output = None
    formatted_date_error = None
    formatting = None

    if request.method == "POST":
        formatting = form.formatting.data.strip()

        if formatting != ">> /dev/null; echo hello!":
            flash(
                "Please input the exact example! Shell injection is risky business!",
                "error",
            )
        else:
            try:
                formatted_date_output = call_date_unsafe(form.formatting.data)
            except RuntimeError as e:
                formatted_date_error = e

    return render_template(
        "/shell/part2.html",
        plain_date_output=plain_date_output,
        form=form,
        formatted_date_output=formatted_date_output,
        formatted_date_error=formatted_date_error,
        formatting=formatting,
    )


@bp_shell.route("/3", methods=["GET", "POST"])
def part3():
    plain_date_output = call_date_safe()

    allowed_commands = [
        "date",
        "uptime",
        "ls",
        "neofetch",
        "echo",
        "whoami",
    ]

    form = ProgramForm(request.form)

    program_result = None

    is_curl = "curl" in request.user_agent.string

    if request.method == "POST":
        program = form.program.data.strip()
        if is_curl:
            if not form.program.data:
                res = "You did not successfully add the form data. Make sure to copy the curl command carefully"
                response = make_response(res, 200)
                response.mimetype = "text/plain"

                return response

            if program not in allowed_commands and not program.startswith("echo"):
                res = "You can only use the following commands:\n"
                for command in allowed_commands:
                    res = res + command + "\n"
                res += (
                    "\nI don't want you to break the server entirely, after all :)\n\n"
                )

                response = make_response(res, 200)
                response.mimetype = "text/plain"

                return response

        try:
            if program.startswith("echo"):
                args = ["echo", program[5:]]
            else:
                args = [program]
            program_result = call_program_safe(args)
        except RuntimeError as e:
            flash("Running the program resulted in an unexpected error: " + e, "error")

        if is_curl:
            res = (
                f"Hi! Here is the result of your CURL request:\n\n{program_result}\n\n"
            )
            res = res + "Looks like you sent the request correctly.\n"
            response = make_response(res, 200)
            response.mimetype = "text/plain"

            return response

    print(request.user_agent.string)

    if not is_curl:
        return render_template(
            "/shell/part3.html",
            plain_date_output=plain_date_output,
            form=form,
            program_result=program_result,
        )

    res = "You seem to have requested the url without any arguments. Make sure to copy the curl command carefully\n\n"

    response = make_response(res, 200)
    response.mimetype = "text/plain"

    return response
