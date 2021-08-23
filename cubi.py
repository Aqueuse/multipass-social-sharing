from flask import Flask
# from flask_talisman import Talisman

import settings

from views.cubiLogin import cubiLogin_blueprint
from views.cubiLogin import cubiLogout_blueprint
from views.cubiAdmin import cubiAdmin_blueprint
from views.cubiAdmin import cubiItemShow_blueprint
from views.cubiAdmin import cubiItemCreate_blueprint
from views.cubiAdmin import cubiItemUpdate_blueprint
from views.cubiAdmin import cubiItemDelete_blueprint
from views.cubiAdmin import cubiCollectionRename_blueprint
from views.cubiAdmin import cubiCollectionDelete_blueprint
from views.cubiAdmin import cubiCollectionCreate_blueprint

app = Flask(__name__, static_folder='static')
app.config['UPLOAD_FOLDER'] = settings.UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = settings.AUTHORIZED_FILES_TYPE
# talisman = Talisman(app, content_security_policy=[])

app.register_blueprint(cubiLogin_blueprint)
app.register_blueprint(cubiLogout_blueprint)
app.register_blueprint(cubiAdmin_blueprint)
app.register_blueprint(cubiItemShow_blueprint)
app.register_blueprint(cubiItemCreate_blueprint)
app.register_blueprint(cubiItemUpdate_blueprint)
app.register_blueprint(cubiItemDelete_blueprint)
app.register_blueprint(cubiCollectionRename_blueprint)
app.register_blueprint(cubiCollectionDelete_blueprint)
app.register_blueprint(cubiCollectionCreate_blueprint)
