from flask import Blueprint, render_template
import settings

home_blueprint = Blueprint('home', __name__,)


@home_blueprint.route('/', methods=['GET'])
def route_to_home():
    return render_template('home.html', baseurl=settings.BASEURL)
