import pprint

from passlib.hash import sha256_crypt
from pymongo import MongoClient
import settings

client = MongoClient('mongodb://localhost:27017/')
db = client[settings.DATABASE]

baseURL = settings.BASEURL
secret = settings.SECRET


# ---------------- users -------------------- #

def validate_user(email, password):
    user_query = list(db.users.find({'email': email}))
    if len(user_query) == 0:
        return False
    else:
        stored_password = user_query[0]["password"]
        if sha256_crypt.verify(password, stored_password):
            return True
    return False


def create_user(email, password):
    encrypted_password = sha256_crypt.hash(password)
    db["users"].insert_one({"email": email, "password": encrypted_password, "user_id": set_id()})


def update_user(email, password):
    print("update "+"/"+email+"/"+password)
    return None


def delete_user(email):
    print("delete "+email)
    return None


# ---------------- tasks -------------------- #

def get_tasks_summary(email):
    raw_result = db["users"].find_one({'email': email}, {'_id': 0})
    if raw_result is None:
        return None
    del raw_result["password"]
    del raw_result["email"]
    del raw_result["user_id"]
    return raw_result


def update_tasks(email, json):
    db["users"].update_one(
        {'email': email},
        {'$set': json}
    )


def get_today_daily_tasks(current_date):
    daily_result = db["users"].find({
        '$or': [
            {
                'facebook.date': {'$lte':  current_date},
                'facebook.repetition.frequency': {'$regex': 'daily'},
            },
            {
                'twitter.date': {'$lte': current_date},
                'twitter.repetition.frequency': {'$regex': 'daily'},
            },
            {
                'instagram.date': {'$lte': current_date},
                'instagram.repetition.frequency': {'$regex': 'daily'},
            }
        ]},
        {'_id': 0}
    )

    cleaned_result = get_frequency_sorted_tasks("daily", list(daily_result))
    return cleaned_result


def get_today_weekly_tasks(current_date, current_day):
    weekly_result = db["users"].find({
        '$or': [
            {
                'facebook.date': {'$lte':  current_date},
                'facebook.repetition.days': {'$regex': current_day},
                'facebook.repetition.frequency': {'$regex': 'weekly'},
            },
            {
                'twitter.date': {'$lte': current_date},
                'twitter.repetition.days': {'$regex': current_day},
                'twitter.repetition.frequency': {'$regex': 'weekly'},
            },
            {
                'instagram.date': {'$lte': current_date},
                'instagram.repetition.days': {'$regex': current_day},
                'instagram.repetition.frequency': {'$regex': 'weekly'},
            }
        ]},
        {'_id': 0}
    )
    cleaned_result = get_frequency_sorted_tasks("weekly", list(weekly_result))
    return cleaned_result


def get_today_monthly_tasks(current_date, current_day_int, current_month):
    monthly_result = db["users"].find({
        '$or': [
            {
                'facebook.date': {'$lte': current_date, '$regex': current_day_int+'T'},
                'facebook.repetition.months': {'$regex': current_month},
                'facebook.repetition.frequency': {'$regex': 'monthly'}
            },
            {
                'twitter.date': {'$lte': current_date},
                'twitter.repetition.months': {'$regex': current_month},
                'twitter.repetition.frequency': {'$regex': 'monthly'}
            },
            {
                'instagram.date': {'$lte': current_date},
                'instagram.repetition.months': {'$regex': current_month},
                'instagram.repetition.frequency': {'$regex': 'monthly'}
            }
        ]},
        {'_id': 0}
    )
    cleaned_result = get_frequency_sorted_tasks("monthly", list(monthly_result))
    return cleaned_result


def get_today_custom_tasks(current_date, current_day, current_month):
    custom_result = db["users"].find({
        '$or': [
            {
                'facebook.date': {'$lte':  current_date},
                'facebook.repetition.days': {'$regex': current_day},
                'facebook.repetition.months': {'$regex': current_month},
                'facebook.repetition.frequency': {'$regex': 'custom'},
            },
            {
                'twitter.date': {'$lte': current_date},
                'twitter.repetition.days': {'$regex': current_day},
                'twitter.repetition.months': {'$regex': current_month},
                'twitter.repetition.frequency': {'$regex': 'custom'},
            },
            {
                'instagram.date': {'$lte': current_date},
                'instagram.repetition.days': {'$regex': current_day},
                'instagram.repetition.months': {'$regex': current_month},
                'instagram.repetition.frequency': {'$regex': 'custom'},
            }
        ]},
        {'_id': 0}
    )
    cleaned_result = get_frequency_sorted_tasks("custom", list(custom_result))
    return cleaned_result


# --------------- log activity -------------- #

def log_task_resume(user_id, task_id, status):
    db.log.insert_one({"user_id": user_id, "task_id": task_id, "status": status})


# ---------------- helpers -------------------- #


def get_max_taskid(social_network_tasks):
    ids = []
    for element in social_network_tasks:
        ids.append(int(element["id"]))
    ids.sort()
    if len(ids) == 0:
        return 0
    if len(ids) > 0:
        ids.sort()
        ids.reverse()
        max_id = ids[0]
        return max_id


def set_id():
    result = list(db["users"].find({}, {'id': 1, '_id': 0}).distinct("id"))
    return get_max_taskid(result) + 1


def get_item_with_int_id(item):
    item['id'] = int(item['id'])
    return item


def get_item_by_filter(json_filter):
    raw_result = db["users"].find_one(json_filter, {'_id': 0})
    if raw_result is None:
        return None
    else:
        return raw_result


def get_frequency_sorted_tasks(frequency, tasks):
    cleaned_result = []

    if len(tasks) > 0:
        for task in tasks:
            for facebook_task in task["facebook"]:
                if facebook_task["repetition"]["frequency"] == frequency:
                    facebook_task["user_id"] = task["user_id"]
                    facebook_task["social_network"] = "facebook"
                    cleaned_result.append(facebook_task)
            for instagram_task in task["instagram"]:
                if instagram_task["repetition"]["frequency"] == frequency:
                    instagram_task["user_id"] = task["user_id"]
                    instagram_task["social_network"] = "instagram"
                    cleaned_result.append(instagram_task)
            for twitter_task in task["twitter"]:
                if twitter_task["repetition"]["frequency"] == frequency:
                    twitter_task["user_id"] = task["user_id"]
                    twitter_task["social_network"] = "twitter"
                    cleaned_result.append(twitter_task)
    return cleaned_result
