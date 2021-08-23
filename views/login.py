from flask import Blueprint, render_template, request, redirect, make_response

import cubiDB
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
        username = request.form["identifiant"]
        password = request.form["password"]
        result = cubiDB.get_item_by_filter("socialSharing", {"username": username})
        if result is None or not cubiDB.validate_user(username, password):
            return render_template("loginFailed.html")
        else:
            response = make_response(redirect(baseURL + username+'/dashboard'))
            response.set_cookie('userID', secret)
            return response


@logout_blueprint.route('/logout/')
def logout():
    # remove cookie session
    response = make_response(redirect(baseURL))
    response.set_cookie('userID', expires=0)
    return response
