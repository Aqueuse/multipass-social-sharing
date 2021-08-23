from flask import Blueprint, render_template, request, redirect, make_response
import cubiDB
import settings

baseURL = settings.BASEURL
secret = settings.SECRET

cubiLogin_blueprint = Blueprint('cubi_login', __name__,)
cubiLogout_blueprint = Blueprint('cubi_logout', __name__,)


@cubiLogin_blueprint.route('/cubi/login/', methods=['GET', 'POST'])
def cubi_login():
    if request.method == 'GET':
        return render_template('cubiLogin.html')
    if request.method == 'POST':
        if cubiDB.validate_user(request.form['identifiant'], request.form['password']):
            response = make_response(redirect(baseURL+'cubi/admin'))
            response.set_cookie('cubi_userID', secret)
            return response
        else:
            return redirect(baseURL)


@cubiLogout_blueprint.route('/cubi/logout/')
def cubi_logout():
    # remove cookie session
    response = make_response(redirect(baseURL+"cubi/login"))
    response.set_cookie('cubi_userID', expires=0)
    return response
