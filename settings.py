import secrets

BASEURL = 'http://127.0.0.1:3000/'
SECRET = secrets.token_urlsafe(64)
UPLOAD_FOLDER = "static/images"
AUTHORIZED_FILES_TYPE = {'png', 'jpg', 'jpeg', 'gif', 'svg'}
DATABASE = 'multipass'
