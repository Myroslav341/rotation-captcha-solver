import os
from uuid import uuid4

from flask import render_template, request, redirect, flash, current_app, url_for, session, jsonify
from werkzeug.utils import secure_filename

from captcha_solver.captcha_solver import append_to_pictures_list, get_picture_by_id, get_solved_picture
from captcha_solver.lib.schema import PictureToSolve
from captcha_solver.view.blueprint import captcha_solver_blueprint


@captcha_solver_blueprint.route('/')
def main_page():
    return render_template("main.html")


@captcha_solver_blueprint.route('/solver', methods=['GET', 'POST'])
def solver_page():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        file_name = secure_filename(file.filename)
        extension = file_name.split(".")[-1]
        file_id = str(uuid4())
        new_file_name = f"{file_id}.{extension}"

        file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], new_file_name))

        file_info = PictureToSolve(file_name=new_file_name, id=file_id)
        append_to_pictures_list(picture=file_info)

        return redirect(url_for("CaptchaSolverViews.solved_captcha_page", picture_id=file_id))
    else:
        return render_template("solver.html")


@captcha_solver_blueprint.route('/solved/<picture_id>', methods=['GET'])
def solved_captcha_page(picture_id: str):
    picture = get_picture_by_id(picture_id=picture_id)

    if not picture:
        picture = get_solved_picture(picture_id=picture_id)

    if not picture:
        flash('No such a file')
        return redirect(url_for("CaptchaSolverViews.solver_page"))

    return render_template(
        "solved_captcha.html",
        file_name=picture.file_name,
        check_url=f"{current_app.config['API_URL']}/is-solved/{picture.id}"
    )


@captcha_solver_blueprint.route('/is-solved/<picture_id>', methods=['GET'])
def solved_captcha_api(picture_id: str):
    picture = get_solved_picture(picture_id=picture_id)

    if not picture:
        return {}

    return jsonify(
        answer=picture.answer,
        rotated_picture_link=f"{current_app.config['API_URL']}/static/{picture.result_picture_file_name}"
    )
