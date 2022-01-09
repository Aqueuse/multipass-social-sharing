from flask import Blueprint, render_template, request, redirect, make_response

import database
import settings

baseURL = settings.BASEURL
secret = settings.SECRET

login_blueprint = Blueprint('login', __name__,)
logout_blueprint = Blueprint('logout', __name__,)


@login_blueprint.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        email = request.form["email"]
        password = request.form["password"]
        result = database.validate_user(email, password)
        if result is None or not database.validate_user(email, password):
            return render_template("loginFailed.html")
        else:
            response = make_response(redirect(baseURL + 'dashboard'))
            response.set_cookie('email', email)
            response.set_cookie('userID', secret)
            return response


@logout_blueprint.route('/logout/')
def logout():
    # remove cookie session
    response = make_response(redirect(baseURL))
    response.set_cookie('email', expires=0)
    response.set_cookie('userID', expires=0)
    return response
