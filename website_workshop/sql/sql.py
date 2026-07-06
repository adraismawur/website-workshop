from sqlite3 import Error

from flask import flash, redirect, render_template, request, url_for
from wtforms import Form, StringField, SubmitField

from website_workshop.util.db import get_db
from website_workshop.sql import bp_sql

class LoginForm(Form):
    username = StringField()
    submit = SubmitField("Login", render_kw={'class': 'btn'})


@bp_sql.route("/1", methods=["GET", "POST"])
def part1():
    db = get_db()

    users = db.execute("SELECT * FROM users  LIMIT 8;").fetchall()

    form = LoginForm(request.form)

    if request.method == "POST":
        r = db.execute("SELECT * FROM users WHERE name = ?", (form.username.data,)).fetchone()
    
        if r is None:
            flash('Failed to log in', 'error')

            return render_template(
                "/sql/part1.html",
                users=users,
                form=form
            )

        flash('Logged in as ' + r[0])

        return redirect(
            url_for('sql.part2', user=r[0]),
        )


    return render_template(
        "/sql/part1.html",
        users=users,
        form=form
    )

@bp_sql.route("/2/<user>", methods=["GET", "POST"])
def part2(user):
    db = get_db()

    form = LoginForm(request.form)

    if request.method == "POST":
        if form.username.data.strip() != "' test--":
            flash("Enter exactly what the prompt says (' test--)", 'error')
            return render_template(
                "/sql/part2.html",
                user=user,
                form=form,
            )

        try:
            r = db.execute("SELECT * FROM users WHERE name = '" + form.username.data.strip() + "';").fetchone()
        except Error as e:
            flash('Failed to log in: ' + str(e), 'warning')
            return redirect(url_for('sql.part3', user=user))
    
        if r is None:
            flash('Failed to log in. Make sure to enter exactly what the prompt says (\' test--)', 'error')

            return render_template(
                "/sql/part1.html",
                user=user,
                form=form
            )

        flash('Logged in as ' + r[0] + '. Looks like you entered a valid user?', 'error')

        return redirect(
            url_for('sql.part2', user=r[0]),
        )

    return render_template(
        "/sql/part2.html",
        user=user,
        form=form,
    )

@bp_sql.route("/3/<user>", methods=["GET", "POST"])
def part3(user):
    db = get_db()

    form = LoginForm(request.form)

    if request.method == "POST":
        if form.username.data.strip() != "' or 1--":
            flash("Enter exactly what the guide says (' or 1--)", 'error')
            return render_template(
                "/sql/part3.html",
                user=user,
                form=form,
            )

        try:
            r = db.execute("SELECT * FROM users WHERE name = '" + form.username.data.strip() + "';").fetchone()
        except Error as e:
            flash('Looks like your input resulted in another error. Make sure to enter exactly what the guide says' + str(e), 'warning')
            return render_template(
                "/sql/part3.html",
                user=user,
                form=form,
            )
    
        if r is None:
            flash('Looks like your input resulted in another error. Make sure to enter exactly what the guide says', 'error')

            return render_template(
                "/sql/part1.html",
                user=user,
                form=form
            )

        flash('Logged in as ' + r[0])

        return redirect(
            url_for('sql.part4', user=r[0]),
        )

    return render_template(
        "/sql/part3.html",
        user=user,
        form=form,
    )

@bp_sql.route("/4/<user>", methods=["GET", "POST"])
def part4(user):
    db = get_db()

    form = LoginForm(request.form)

    if request.method == "POST":
        has_correct_beginning = form.username.data.strip().startswith("'; INSERT INTO users (name) values ('")
        has_correct_end = form.username.data.strip().endswith("');--")


        
        if not has_correct_beginning or not has_correct_end:
            flash("Enter exactly what the guide says ('; INSERT INTO users (name) values ('test');--). You can replace 'test'", 'error')
            return render_template(
                "/sql/part4.html",
                user=user,
                form=form,
            )

        try:
            r = db.execute("SELECT * FROM users WHERE name = '" + form.username.data.strip() + "';").fetchone()
        except Error as e:
            flash('Error: ' + str(e), 'warning')
            return redirect(url_for('sql.part5', user=user))
    
        if r is None:
            flash('Failed to log in', 'error')

            return render_template(
                "/sql/part1.html",
                user=user,
                form=form
            )

        flash('Logged in as ' + r[0])

        return redirect(
            url_for('sql.part4', user=r[0]),
        )

    return render_template(
        "/sql/part4.html",
        user=user,
        form=form,
    )

@bp_sql.route("/5/<user>", methods=["GET", "POST"])
def part5(user):
    db = get_db()

    form = LoginForm(request.form)

    if request.method == "POST":
        has_correct_beginning = form.username.data.strip().startswith("'; INSERT INTO users (name) values ('")
        has_correct_end = form.username.data.strip().endswith("');--")


        
        if not has_correct_beginning or not has_correct_end:
            flash("Enter exactly what the guide says ('; INSERT INTO users (name) values ('test');--)", 'error')
            return render_template(
                "/sql/part5.html",
                user=user,
                form=form,
            )

        try:
            r = db.executescript("SELECT * FROM users WHERE name = '" + form.username.data.strip() + "';").fetchone()
        except Error as e:
            flash('Error: ' + str(e), 'warning')
            return redirect(url_for('sql.part6', user=user))
    
        if r is None:
            flash('Failed to log in', 'warning')

            return redirect(url_for('sql.part6', user=user))

        flash('Logged in as ' + r[0])

        return redirect(
            url_for('sql.part4', user=r[0]),
        )

    return render_template(
        "/sql/part5.html",
        user=user,
        form=form,
    )

@bp_sql.route("/6/<user>", methods=["GET", "POST"])
def part6(user):
    db = get_db()

    form = LoginForm(request.form)


    users = db.execute("SELECT * FROM users;").fetchall()

    form = LoginForm(request.form)

    if request.method == "POST":
        r = db.execute("SELECT * FROM users WHERE name = ?;", (form.username.data,)).fetchone()
    
        if r is None:
            flash('Failed to log in', 'error')

            return redirect(
                url_for('sql.part6', user=user),
            )

        flash('Logged in as ' + r[0])

        return redirect(
            url_for('sql.part6', user=r[0]),
        )

    return render_template(
        "/sql/part6.html",
        user=user,
        form=form,
        users=users,
    )
