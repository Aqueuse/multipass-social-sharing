import datetime
import os

from flask import Blueprint, render_template, redirect, request
from werkzeug.utils import secure_filename

import database
import settings

baseURL = settings.BASEURL
upload_folder = settings.UPLOAD_FOLDER
secret = settings.SECRET

tasks_blueprint = Blueprint('user', __name__, )
task_create_blueprint = Blueprint('task_create', __name__, )
task_duplicate_blueprint = Blueprint('task_duplicate', __name__, )
task_edit_blueprint = Blueprint('task_edit', __name__, )
task_delete_blueprint = Blueprint('task_delete', __name__, )

task = {
    "date": datetime.datetime.now().replace(second=0, microsecond=0).isoformat(),
    "imagesList": [],
    "message": "mon message",
    "repetition": {
        "days": "MO,TU,WE,TH, FR, SA, SU",
        "months": "JAN, FEB, MAR, APR, MAY, JUN, JUL, AUG, SEP, OCT, NOV, DEC",
        "frequency": "weekly"
    },
    "id": 0,
    "taskname": "mon Premier Post"
}


@tasks_blueprint.route('/dashboard', methods=['GET'])
def route_to_user_tasks():
    if request.cookies.get('userID') == secret:
        email = request.cookies.get('email')
        dict_tasks_summary = database.get(email)
        return render_template(
            'tasks.html',
            baseurl=baseURL,
            email=email,
            dict_tasks_summary=dict_tasks_summary
        )
    else:
        return redirect(baseURL + "login")


@task_edit_blueprint.route('/<social_network>/edit', methods=['POST'])
def route_to_edit_task(social_network):
    if request.cookies.get('userID') == secret:
        social_network = social_network
        email = request.cookies.get('email')
        id = request.form["id"]
        message = request.form["message"]
        taskname = request.form["taskname"]
        date = request.form["date"]
        repetition_frequency = request.form["repetition_frequency"]
        days = request.form["days"]
        months = request.form["months"]
        files = request.files.getlist("files[]")

        tasks = database.get_item_by_filter({"email": email})
        for element in tasks[social_network]:
            if element["id"] == float(id):
                element["taskname"] = taskname
                element["message"] = message
                element["date"] = date
                element["repetition"]["frequency"] = repetition_frequency
                element["repetition"]["days"] = days
                element["repetition"]["months"] = months
                if len(files) > 1:
                    images_list = []
                    for file in files:
                        file.save(os.path.join(upload_folder, email, secure_filename(file.filename)))
                        images_list.append(secure_filename(file.filename))
                    element["imagesList"] = images_list
                if len(files) <= 1:
                    element["imagesList"] = []
        database.update_tasks(email, tasks)
        return redirect("/dashboard")
    else:
        return redirect(baseURL)


@task_duplicate_blueprint.route('/<social_network>/duplicate', methods=['POST'])
def route_to_duplicate_task(social_network):
    if request.cookies.get('userID') == secret:
        email = request.cookies.get('email')
        id = request.form['id']
        tasks = database.get_item_by_filter({'email': email})
        for element in tasks[social_network]:
            if element['id'] == float(id):
                duplicate_task = {
                    "taskname": element['taskname'],
                    "message": element['message'],
                    "date": element['date'],
                    "repetition": element['repetition'],
                    "imagesList": element['imagesList'],
                    "id": database.get_max_taskid(tasks[social_network])+1
                }
                tasks[social_network].append(duplicate_task)
        database.update_tasks(email, tasks)
        return redirect("/dashboard")
    else:
        return redirect(baseURL)


@task_delete_blueprint.route('/<social_network>/delete', methods=['POST'])
def route_to_delete_task(social_network):
    if request.cookies.get('userID') == secret:
        email = request.cookies.get('email')
        id = request.form["id"]
        tasks = database.get_item_by_filter({"email": email})
        for index, element in enumerate(tasks[social_network]):
            if element["id"] == float(id):
                tasks[social_network].pop(index)
        database.update_tasks(email, tasks)
        return redirect("/dashboard")
    else:
        return redirect(baseURL)


@task_create_blueprint.route('/<social_network>/create', methods=['GET'])
def route_to_create_task(social_network):
    if request.cookies.get('userID') == secret:
        email = request.cookies.get('email')
        tasks = database.get_item_by_filter({"email": email})
        tasks[social_network].append(task)
        database.update_tasks(email, tasks)
        return redirect("/dashboard")
    else:
        return redirect(baseURL)
