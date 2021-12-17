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
    db["users"].insert_one({"email": email, "password": encrypted_password, "id": set_id()})


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
    return raw_result


def update_tasks(email, json):
    db["users"].update_one(
        {'email': email},
        {'$set': json}
    )


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
