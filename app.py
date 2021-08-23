from views.home import home_blueprint
from views.login import login_blueprint, logout_blueprint
from views.tasks import tasks_blueprint, task_create_blueprint,\
    task_edit_blueprint, task_delete_blueprint, task_duplicate_blueprint

import settings
import cubi

app = cubi.app

app.config['UPLOAD_FOLDER'] = '/static/images'
app.config['SESSION_COOKIE_NAME'] = 'userSession'
app.config['SECRET_KEY'] = settings.SECRET

app.register_blueprint(home_blueprint)
app.register_blueprint(login_blueprint)
app.register_blueprint(logout_blueprint)

app.register_blueprint(tasks_blueprint)
app.register_blueprint(task_create_blueprint)
app.register_blueprint(task_edit_blueprint)
app.register_blueprint(task_duplicate_blueprint)
app.register_blueprint(task_delete_blueprint)


if __name__ == '__main__':
    app.run()
