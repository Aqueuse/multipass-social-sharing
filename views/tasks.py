import os
import time
import pprint

from flask import Blueprint, render_template, redirect, request
from werkzeug.utils import secure_filename

import cubiDB
import database
import settings

baseURL = settings.BASEURL
secret = settings.SECRET
upload_folder = settings.UPLOAD_FOLDER

tasks_blueprint = Blueprint('user', __name__, )
task_create_blueprint = Blueprint('task_create', __name__, )
task_duplicate_blueprint = Blueprint('task_duplicate', __name__, )
task_edit_blueprint = Blueprint('task_edit', __name__, )
task_delete_blueprint = Blueprint('task_delete', __name__, )

task = {
    "date": time.strftime("%Y-%m-%d"),
    "imagesList": [],
    "message": "mon message",
    "repetition": {
        "days": "MO,TU,WE,TH, FR, SA, SU",
        "months": "JAN, FEB, MAR, APR, MAY, JUN, JUL, AUG, SEP, OCT, NOV, DEC",
        "type": "weekly"
    },
    "taskid": 0,
    "taskname": "mon Premier Post",
    "time": "20:00"
}


@tasks_blueprint.route('/<username>/dashboard', methods=['GET'])
def route_to_user_tasks(username):
    if request.cookies.get('userID') == secret:
        dict_tasks_summary = database.get_tasks_summary(username)
        return render_template(
            'tasks.html',
            baseurl=settings.BASEURL,
            username=username,
            dict_tasks_summary=dict_tasks_summary
        )
    else:
        return redirect(baseURL + "login")


@task_create_blueprint.route('/<username>/<social_network>/create', methods=['GET'])
def route_to_create_task(username, social_network):
    if request.cookies.get('userID') == secret:
        tasks = cubiDB.get_item_by_filter("socialSharing", {"username": username})
        id = tasks["id"]
        tasks[social_network].append(task)
        database.update_tasks(id, tasks)
        return redirect("/" + username + "/dashboard")
    else:
        return redirect(baseURL)


@task_edit_blueprint.route('/<username>/<social_network>/<taskid>/edit', methods=['POST'])
def route_to_edit_task(username, social_network, taskid):
    if request.cookies.get('userID') == secret:
        social_network = social_network
        message = request.form["message"]
        task_name = request.form["task_name"]
        date = request.form["date"]
        task_time = request.form["time"]
        repetition_type = request.form["repetition_type"]
        days = request.form["days"]
        months = request.form["months"]
        files = request.files.getlist("files[]")

        tasks = cubiDB.get_item_by_filter("socialSharing", {"username": username})
        id = tasks["id"]
        for element in tasks[social_network]:
            if element["taskid"] == int(taskid):
                element["taskname"] = task_name
                element["message"] = message
                element["date"] = date
                element["time"] = task_time
                element["repetition"]["type"] = repetition_type
                element["repetition"]["days"] = days
                element["repetition"]["months"] = months
                if len(files) > 1:
                    images_list = []
                    for file in files:
                        file.save(os.path.join(upload_folder, username, secure_filename(file.filename)))
                        images_list.append(secure_filename(file.filename))
                    element["imagesList"] = images_list
                if len(files) <= 1:
                    element["imagesList"] = []
        database.update_tasks(id, tasks)
        return redirect("/" + username + "/dashboard")
    else:
        return redirect(baseURL)


@task_duplicate_blueprint.route('/<username>/<social_network>/<taskid>/duplicate', methods=['POST'])
def route_to_duplicate_task(username, social_network, taskid):
    if request.cookies.get('userID') == secret:
        tasks = cubiDB.get_item_by_filter("socialSharing", {"username": username})
        id = tasks["id"]
        for element in tasks[social_network]:
            if element["taskid"] == int(taskid):
                duplicate_task = {
                    "taskname": element["taskname"],
                    "message": element["message"],
                    "date": element["date"],
                    "time": element["time"],
                    "repetition": element["repetition"],
                    "imagesList": element["imagesList"],
                    "taskid": database.get_max_taskid(tasks[social_network])+1
                }
                tasks[social_network].append(duplicate_task)
        database.update_tasks(id, tasks)
        return redirect("/" + username + "/dashboard")
    else:
        return redirect(baseURL)


@task_delete_blueprint.route('/<username>/<social_network>/<taskid>/delete', methods=['POST'])
def route_to_delete_task(username, social_network, taskid):
    if request.cookies.get('userID') == secret:
        tasks = cubiDB.get_item_by_filter("socialSharing", {"username": username})
        id = tasks["id"]
        for index, element in enumerate(tasks[social_network]):
            if str(element["taskid"]) == str(taskid):
                tasks[social_network].pop(index)
        database.update_tasks(id, tasks)
        return redirect("/" + username + "/dashboard")
    else:
        return redirect(baseURL)
