from passlib.hash import sha256_crypt
import uuid
from pymongo import MongoClient
import settings

client = MongoClient('mongodb://localhost:27017/')
db = client[settings.DATABASE]


# ----------- Users ------- #

def validate_user(username, password):
    user_query = list(db.users.find({'username': username}))
    if len(user_query) == 0:
        return False
    else:
        stored_password = user_query[0]["password"]
        if sha256_crypt.verify(password, stored_password):
            return True
    return False


def create_user(username, password):
    #encrypted_password = sha256_crypt.encrypt(password)     DEPRECATED
    encrypted_password = sha256_crypt.hash(password)
    db["users"].insert_one({"username": username, "password": encrypted_password, "id": set_id("users")})


# ---------- collection operations ------ #

def get_ids(collection):
    ids = []
    result = list(db[collection].find({}, {'id': 1, '_id': 0}))
    for element in result:
        ids.append(int(element["id"]))
    ids.sort()
    return ids


def get_all_collections_names():
    return db.list_collection_names()


def get_collection(collection):
    return list(db[collection].find({}))


def create_collection(collection, json):
    db[collection].insert_one(json)


def remove_collection(collection):
    db[collection].drop()


def rename_collection(collection, new_name):
    db[collection].rename(new_name)


# --------- items operations ---------- #

def get_item(collection, id):
    raw_result = db[collection].find_one({'id': int(id)}, {'_id': 0})
    result = item_with_int_id(raw_result)
    return result


def get_item_by_filter(collection, json_filter):
    raw_result = db[collection].find_one(json_filter, {'_id': 0})
    if raw_result is None:
        return None
    else:
        result = item_with_int_id(raw_result)
        return result


def get_all_items(collection):
    result = list(db[collection].find({}, {'_id': 0}))
    return result


def get_keys_from_collection(collection, key):
    result = list(db[collection].find({}, key).sort('date', -1))
    return result


def count_items(collection, key, value):
    return db[collection].count_documents({key: value})


def create_item(collection, json):
    db[collection].insert_one(json)


def update_item(collection, id, json):
    db[collection].update_one(
        {'id': int(id)},
        {'$set': json}
    )


def remove_item(collection, id):
    db[collection].remove({'id': int(id)})


# -------- Helpers ------- #

def set_id(collection):
    result = list(db[collection].find({}, {'id': 1, '_id': 0}).distinct("id"))
    return get_max_id(result) + 1


def item_with_int_id(item):
    id = int(item['id'])
    item['id'] = id
    return item


def get_max_id(ids_array):
    if len(ids_array) == 0:
        return 0
    if len(ids_array) > 0:
        ids_array.sort()
        ids_array.reverse()
        max_id = ids_array[0]
        return max_id


def get_min_id(ids_array):
    ids_array.sort()
    min_id = ids_array[0]
    return min_id


def get_ancestor_item(collection):
    ids = get_ids(collection)
    min_id = get_min_id(ids)
    result = get_item(collection, min_id)
    return result


def duplicate_item(collection):
    json = get_ancestor_item(collection)
    json['id'] = set_id(collection)
    create_item(collection, json)


def create_unique_id(complicated_title):
    key = "-" + uuid.uuid4().hex[:8]

    short_title = complicated_title.lower()
    array_title = short_title.split(" ")[:3]
    clean_title = []

    for word in array_title:
        for char in word:
            if char.isalnum():
                clean_title.append(char)
    return "".join(clean_title) + key
