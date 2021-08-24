from flask import Blueprint, render_template, request, make_response, redirect

import cubiDB
import database
import settings

baseURL = settings.BASEURL
secret = settings.SECRET

user_account_blueprint = Blueprint('user_account', __name__, )


@user_account_blueprint.route('/<username>/account', methods=['GET'])
def route_to_user_account(username):
    if request.cookies.get('userID') == secret:
        email = database.get_user_email(username)
        return render_template('userAccount.html', username=username, email=email)
    else:
        response = make_response(redirect(baseURL + username + '/dashboard'))
        response.set_cookie('userID', secret)
        return response
