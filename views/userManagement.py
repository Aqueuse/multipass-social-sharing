from flask import Blueprint, render_template, request, make_response, redirect
import settings
import database

baseURL = settings.BASEURL

user_account_blueprint = Blueprint('user_account', __name__,)
user_account_create_blueprint = Blueprint('user_account_create', __name__,)
user_account_edit_blueprint = Blueprint('user_account_edit', __name__,)


@user_account_blueprint.route('/<username>/account', methods=['GET'])
def route_to_account(username):
    email = database.get_user_email(username)
    return render_template('userAccount.html', baseurl=baseURL, username=username, email=email)


@user_account_create_blueprint.route('/register', methods=['GET', 'POST'])
def route_to_create_account():
    if request.method == 'GET':
        return render_template('createUser.html', baseurl=settings.BASEURL)
    if request.method == 'POST':
        email = request.form["email"]
        password = request.form["password"]

        if not database.user_exist(email):
            database.create_user(email, password)
            response = make_response(redirect(baseURL + 'login'))
            response.set_cookie('email', email)
            response.headers["message"] = "account created, please login"
            return response
        else:
            response = make_response(redirect(baseURL + 'login'))
            response.set_cookie('email', email)
            response.headers["message"] = "account already exist, please login"
            return response


@user_account_edit_blueprint.route('/<username>/edit', methods=['POST'])
def route_to_edit_account():
    email = request.form["email"]
    password = request.form["password"]
    database.update_user(email, password)
    return render_template('login.html', baseurl=baseURL, validation_message="user account edited")
