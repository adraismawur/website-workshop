from flask import (
    current_app,
    flash,
    redirect,
    render_template,
    request,
    send_file,
    url_for,
)
from wtforms import FileField, Form, SubmitField
from uuid import uuid4
from website_workshop.files import bp_files
from pathlib import Path
from subprocess import run

from website_workshop.util.config import Config


class FastaForm(Form):
    file = FileField(render_kw={"accept": ".fa,.fasta", "class": "btn"})
    submit = SubmitField("Upload", render_kw={"class": "btn"})


@bp_files.route("/1", methods=["GET", "POST"])
def part1():

    form = FastaForm(request.form)

    if request.method == "POST":
        filename = form.file.data

        is_fasta = filename.endswith(".fa") or filename.endswith(".fasta")
        if not is_fasta:
            flash("File is not a fasta file", "warning")
        else:
            flash("File is a fasta file! Hopefully!")

    return render_template(
        "/files/part1.html",
        form=form,
    )


@bp_files.route("/2", methods=["GET", "POST"])
def part2():
    form = FastaForm(request.form)

    if request.method == "POST":
        if "file" not in request.files:
            flash("no file uploaded", "error")
            return redirect(request.url)

        file = request.files["file"]

        if file.name == "":
            flash("no file uploaded", "error")
            return redirect(request.url)

        filename = file.filename

        print(filename)

        is_fasta = filename.endswith(".fa") or filename.endswith(".fasta")
        if not is_fasta:
            flash("File is not a fasta file", "warning")
        else:
            guid = uuid4()

            job_folder: Path = Path(Config.UPLOAD_FOLDER) / str(guid)

            job_folder.mkdir(parents=True)

            input_file_path = job_folder / filename

            file.save(input_file_path)

            out = run(["wc", "-l", input_file_path], capture_output=True)

            with open(job_folder / "results.txt", "w") as f:
                f.write(out.stdout.decode("utf-8"))

            flash("File uploaded!")

            return redirect(
                url_for("files.part3_summary", guid=guid, filename=filename)
            )

    return render_template(
        "/files/part2.html",
        form=form,
    )


@bp_files.route("/3/summary/<guid>/<filename>", methods=["GET", "POST"])
def part3_summary(guid: str, filename: str):
    form = FastaForm(request.form)

    return render_template(
        "/files/part3.html",
        form=form,
        guid=guid,
        filename=filename,
    )


@bp_files.route("/3/view/<guid>/<filename>", methods=["GET", "POST"])
def part3_view(guid: str, filename: str):
    form = FastaForm(request.form)

    job_folder: Path = Path(Config.UPLOAD_FOLDER) / str(guid)

    input_file_path = job_folder / filename

    return send_file(
        input_file_path,
        mimetype="text/plain",
    )


@bp_files.route("/4", methods=["GET", "POST"])
def part4():

    return render_template(
        "/files/part4.html",
    )
