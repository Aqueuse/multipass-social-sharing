import uuid

BASEURL = 'http://127.0.0.1:3000/'
SECRET = uuid.uuid4().hex[:16]
UPLOAD_FOLDER = "static/images"
AUTHORIZED_FILES_TYPE = {'png', 'jpg', 'jpeg', 'gif', 'svg'}
DATABASE = 'multipass'
