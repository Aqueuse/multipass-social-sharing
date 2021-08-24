import cubiDB
import settings

baseURL = settings.BASEURL
secret = settings.SECRET

# ---------------- users -------------------- #

def create_user(username, email, password):
    print("create "+username+"/"+email+"/"+password)
    return None


def update_user(username, email, password):
    print("update "+username+"/"+email+"/"+password)
    return None


def delete_user(username):
    print("delete "+username)
    return None


def get_user_email(username):
    user = cubiDB.get_item_by_filter('socialSharing', {'username': username})
    if len(user) > 0:
        return user["email"]
    else:
        return "user not found"

# ---------------- tasks -------------------- #


def get_tasks_summary(username):
    result = cubiDB.get_item_by_filter("socialSharing", {"username": username})
    del result["username"]
    del result["password"]
    del result["email"]
    del result["id"]
    return result


def update_tasks(id, json):
    cubiDB.update_item("socialSharing", id, json)


# ---------------- helpers -------------------- #


def get_max_taskid(social_network_tasks):
    ids = []
    for element in social_network_tasks:
        ids.append(int(element["taskid"]))
    ids.sort()
    if len(ids) == 0:
        return 0
    if len(ids) > 0:
        ids.sort()
        ids.reverse()
        max_id = ids[0]
        return max_id
