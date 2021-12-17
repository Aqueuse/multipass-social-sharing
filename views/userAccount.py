from flask import Blueprint, render_template, request, make_response, redirect

import settings

baseURL = settings.BASEURL
secret = settings.SECRET

user_account_blueprint = Blueprint('user_account', __name__, )


@user_account_blueprint.route('/account', methods=['GET'])
def route_to_user_account():
    if request.cookies.get('userID') == secret:
        email = request.cookies.get('email')
        return render_template('userAccount.html', email=email)
    else:
        response = make_response(redirect(baseURL + '/dashboard'))
        response.set_cookie('userID', secret)
        return response
