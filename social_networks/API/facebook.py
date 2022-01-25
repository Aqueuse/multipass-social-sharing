from database import log_task_resume


def share_to_fb(task):
    print("connect to the facebook API")
    print("get_token()  ")
    print("share message")
    print("retrieve status")
    user_id = 0
    task_id = 0
    status = "success"
    log_task_resume(user_id, task_id, status)
