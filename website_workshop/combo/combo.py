import hashlib
from os import remove
from pathlib import Path
from subprocess import run
from uuid import uuid4

from flask import flash, make_response, redirect, render_template, request, send_file, url_for
from wtforms import FileField, Form, SelectField, SubmitField

from website_workshop.combo import bp_combo
from website_workshop.util.config import Config

class FastaForm(Form):
    file = FileField(render_kw={"accept": ".fa,.fasta", "class": "btn"})
    submit = SubmitField("Upload", render_kw={"class": "btn"})

class ProgramForm(Form):
    program = SelectField(
        choices=[
            "wc",
            "stat",
        ],
    )
    submit = SubmitField("Run", render_kw={"class": "btn"})

def call_program_safe(args):
    out = run(args, capture_output=True)

    if out.returncode != 0:
        output = out.stderr.decode("utf-8")
        raise RuntimeError(
            f"Failed to run {args} command: {output}"
        )

    return out.stdout.decode("utf-8")

def call_program_unsafe(program: str):
    out = run(program, capture_output=True, shell=True)

    if out.returncode != 0:
        output = out.stderr.decode("utf-8")
        raise RuntimeError(
            f"Failed to run {program} command: {output}"
        )

    return out.stdout.decode("utf-8")


@bp_combo.route("/1", methods=["GET", "POST"])
def part1():
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

            job_folder: Path = Path(Config.COMBO_UPLOAD_FOLDER) / str(guid)

            job_folder.mkdir(parents=True)

            input_file_path = job_folder / filename

            file.save(input_file_path)

            flash("File uploaded!")

            return redirect(
                url_for("combo.part2", guid=guid, filename=filename)
            )
        
    return render_template(
        "/combo/part1.html",
        form=form
    )

@bp_combo.route("/2/<guid>/<filename>", methods=["GET", "POST"])
def part2(guid: str, filename: str):

    allowed_commands = [
        "wc",
        "stat",
    ]

    form = ProgramForm(request.form)

    program_result = None
    program_error = None

    if request.method == "POST":
        is_curl = "curl" in request.user_agent.string
        if is_curl:
            res = "Not so fast, wait until the next part :)"
            response = make_response(res, 200)
            response.mimetype = "text/plain"

            return response

        if form.program.data not in allowed_commands:
            flash(f'unexpected command: {form.program.data}', 'warning')
        else:
            try:

                job_folder: Path = Path(Config.COMBO_UPLOAD_FOLDER) / str(guid)

                input_file_path = job_folder / filename

                program_result = call_program_safe([form.program.data, input_file_path.relative_to(Path.cwd())])
            except RuntimeError as e:
                program_error = f"Running the command resulted in an error: {e}"

            


    return render_template(
        "/combo/part2.html",
        form=form,
        guid=guid,
        filename=filename,
        program_result=program_result,
        program_error=program_error,
    )

@bp_combo.route("/3", methods=["GET", "POST"])
def part3():
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

            job_folder: Path = Path(Config.COMBO_UPLOAD_FOLDER) / str(guid)

            job_folder.mkdir(parents=True)

            input_file_path = job_folder / filename

            file.save(input_file_path)

            sha1 = hashlib.sha1()
            BUF_SIZE = 65536

            with open(input_file_path, 'rb') as f:
                while True:
                    data = f.read(BUF_SIZE)
                    if not data:
                        break
                    sha1.update(data)
            
            expected_hash = "ca3c348846366038dbe133cba46b84e0e6c075b3"

            if sha1.hexdigest() != expected_hash:
                remove(input_file_path)
                flash('Uploaded file did not have matching hash. Are you sure you are uploading the right file?', 'error')

                return redirect(request.url)

            flash("File uploaded!")

            return redirect(
                url_for("combo.part4", guid=guid, filename=filename)
            )
        
    return render_template(
        "/combo/part3.html",
        form=form
    )

@bp_combo.route("/example_file_download", methods=["GET"])
def download_script():
    return send_file(Config.COMBO_SCRIPT_LOCATION)

@bp_combo.route("/4/<guid>/<filename>", methods=["GET", "POST"])
def part4(guid: str, filename: str):
    allowed_programs = [
        'bash',
        'wc',
        'stat'
    ]

    form = ProgramForm(request.form)

    program_result = None
    program_error = None

    if request.method == "POST":
        is_curl = "curl" in request.user_agent.string

        if form.program.data not in allowed_programs:
            flash(f'unexpected command: {form.program.data}', 'error')
        else:
            try:

                job_folder: Path = Path(Config.COMBO_UPLOAD_FOLDER) / str(guid)

                input_file_path = job_folder / filename

                program_result = call_program_safe([form.program.data, input_file_path.relative_to(Path.cwd())])


                if is_curl:
                    res = program_result
                    response = make_response(res, 200)
                    response.mimetype = "text/plain"

                    return response

            except RuntimeError as e:
                program_error = f"Running the command resulted in an error: {e}"


    return render_template(
        "/combo/part4.html",
        form=form,
        guid=guid,
        filename=filename,
        program_result=program_result,
        program_error=program_error,
    )



