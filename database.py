import datetime
from passlib.hash import sha256_crypt
import sqlite3

connection = sqlite3.connect('/srv/multipass.db')


# ------------------ Users ----------------- #

def get_user(email):
    global connection
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE email=" + email)
    user = cursor.fetchall()
    return user


def validate_user(email, password):
    user_query = get_user(email)
    if user_query is None:
        return False
    else:
        stored_password = user_query.password
        if sha256_crypt.verify(password, stored_password):
            return True
    return False


def create_user(email, password):
    encrypted_password = sha256_crypt.hash(password)

    sql = ''' INSERT INTO users(email, password) VALUES(?,?) '''
    user = (email, encrypted_password)

    cursor = connection.cursor()
    cursor.execute(sql, user)
    connection.commit()


def update_user(email, password):
    user = (password, email)
    sql = ''' UPDATE users SET password = ? WHERE email = ?'''
    cursor = connection.cursor()
    cursor.execute(sql, user)
    connection.commit()


def delete_user(email):
    User.delete_user(email)


def user_exist(email):
    return User.user_exist(email)


# ------------------ Tasks ----------------- #

def get_user_tasks(email):
    cur.execute("SELECT * FROM basicTask WHERE user_id=?", (email,))
    cursor = connection.cursor()
    cursor.execute()

    user_tasks = cursor.fetchall()

    if len(user_tasks) == 0:
        return get_task_dict(true)

    for task in user_tasks:
        print(task)
        user_tasks_list.append(task_to_dict(task.task_id))

    return user_tasks_list


def create_task(task_id, user_id, name, date, repetition, days, months):
    sql = ''' INSERT INTO basicTask(task_id, user_id, name, date, repetition, days, months) VALUES(?,?,?,?,?,?,?) '''
    task = (task_id, user_id, name, date, repetition, days, months)

    cursor = connection.cursor()
    cursor.execute(sql, task)
    connection.commit()

    # if "facebook" in task:
    #     create_facebook_task(
    #         task["task_id"],
    #         task.facebook["facebook-message"],
    #         task.facebook["facebook-files"]
    #     )
    # if "twitter" in task:
    #     create_twitter_task(
    #         task["task_id"],
    #         task.twitter["twitter-message"],
    #         task.twitter["twitter-files"]
    #     )
    # if "instagram" in task:
    #     create_instagram_task(
    #         task["task_id"],
    #         task["instagram"]["instagram-message"],
    #         task["instagram"]["instagram-files"]
    #     )


def update_task(task_id, user_id, name, date, repetition, days, months):
    if basic_task_exist(task_id):
        task = (task_id, user_id, name, date, repetition, days, months)
        sql = ''' UPDATE basicTask SET name = ?, date = ?, repetition = ?, days= ?, months=? WHERE task_id = ?'''
        cur = conn.cursor()
        cur.execute(sql, task)
        conn.commit()

        # if task["facebook"]:
        #     FacebookTask.update_facebook_task(
        #         task["task_id"],
        #         task.facebook["facebook-message"],
        #         task.facebook["facebook-files"]
        #     )
        # if task["twitter"]:
        #     TwitterTask.update_twitter_task(
        #         task["task_id"],
        #         task.twitter["twitter-message"],
        #         task.twitter["twitter-files"]
        #     )
        # if task["instagram"]:
        #     InstagramTask.update_instagram_task(
        #         task["task_id"],
        #         task.instagram["instagram-message"],
        #         task.instagram["instagram-files"]
        #     )


def delete_basic_task(task_id):
    sql = 'DELETE FROM basicTask WHERE task_id=?'
    cur = conn.cursor()
    cur.execute(sql, (task_id,))
    conn.commit()

    # if FacebookTask.facebook_task_exist(task_id):
    #     FacebookTask.delete_facebook_task(task_id)
    # if TwitterTask.twitter_task_exist(task_id):
    #     TwitterTask.delete_twitter_task(task_id)
    # if InstagramTask.instagram_task_exist(task_id):
    #     InstagramTask.delete_instagram_task(task_id)


def get_max_task_id():
    return BasicTask.get_max_task_id()


def get_frequency_sorted_tasks(frequency, tasks):
    print("not implemented")


def get_today_daily_tasks(current_date):
    print("not implemented")


def get_today_weekly_tasks(current_date, current_day):
    print("not implemented")


def get_today_monthly_tasks(current_date, current_day_int, current_month):
    print("not implemented")


def get_today_custom_tasks(current_date, current_day, current_month):
    print("not implemented")

# --------------- log activity -------------- #

# def log_task_resume(user_id, task_id, status):
#     db.log.insert_one({"user_id": user_id, "task_id": task_id, "status": status})


# --------------- helpers -------------- #

def get_task_dict(empty, task_id=0, user_id=None, name="my_task", date="2022-01-14T20:38", repetition="daily", days="MO", months="JAN"):
    task = {
        'task_id': 0,
        'user_id': None,
        'task_name': 'my task',
        'date': datetime.datetime.now().replace(second=0, microsecond=0).isoformat(),
        'repetition': 'daily',
        'days': 'MO',
        'months': 'JAN',
        'facebook': {
            'isActive': False,
            'message': 'my message',
            'files_list': ""
        },
        'instagram': {
            'isActive': False,
            'message': 'my message',
            'files_list': ""
        },
        'twitter': {
            'isActive': False,
            'message': 'my message',
            'files_list': ""
        }
    }

    if empty:
        return task

    if not empty:
        if basic_task_exist(task_id):
            task["task_id"] = task_id
            task["user_id"] = user_id
            task["name"] = name
            task["date"] = date
            task["repetition"] = repetition
            task["days"] = days
            task["months"] = months

            # if facebook_task_exist(task_id):
            #     facebook_task = get_facebook_task(task_id)
            #     task["facebook"]["isActive"] = True
            #     task["facebook"]["message"] = facebook_message
            #     task["facebook"]["files"] = facebook_files
            # if twitter_task_exist(task_id):
            #     twitter_task = get_twitter_task(task_id)
            #     task["twitter"]["isActive"] = True
            #     task["twitter"]["message"] = twitter_message
            #     task["twitter"]["files"] = twitter_files
            # if instagram_task_exist(task_id):
            #     instagram_task = get_instagram_task(task_id)
            #     task["instagram"]["isActive"] = True
            #     task["instagram"]["message"] = instagram_message
            #     task["instagram"]["files"] = instagram_files
    return task
