from flask import Blueprint, render_template, request
import settings

import database

account_blueprint = Blueprint('task', __name__,)
account_edit_blueprint = Blueprint('task_edit', __name__,)


@account_blueprint.route('/<username>/account', methods=['GET'])
def route_to_account(username):
    email = database.get_user_email(username)
    return render_template('userAccount.html', baseurl=settings.BASEURL, username=username, email=email)


@account_edit_blueprint.route('/<username>/account', methods=['POST'])
def route_to_edit_account(username):
    email = request.form["email"]
    password = request.form["password"]
    database.update_user(username, email, password)
    return render_template('tasks.html', baseurl=settings.BASEURL, validation_message="user account updated")
