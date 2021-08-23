import json
from flask import Blueprint, render_template, request, redirect

import cubiDB
import settings

baseURL = settings.BASEURL
secret = settings.SECRET

cubiAdmin_blueprint = Blueprint('admin', __name__, )

cubiItemShow_blueprint = Blueprint('item_show', __name__, )
cubiItemCreate_blueprint = Blueprint('item_create', __name__, )
cubiItemUpdate_blueprint = Blueprint('item_update', __name__, )
cubiItemDelete_blueprint = Blueprint('item_delete', __name__, )

cubiCollectionRename_blueprint = Blueprint('collection_rename', __name__, )
cubiCollectionDelete_blueprint = Blueprint('collection_delete', __name__, )
cubiCollectionCreate_blueprint = Blueprint('collection_create', __name__, )


@cubiAdmin_blueprint.route('/cubi/admin', methods=['GET'])
def show_admin_page():
    if request.cookies.get('cubi_userID') == secret:
        collections_ids = []
        for element in cubiDB.get_all_collections_names():
            collections_ids.append(cubiDB.get_ids(element))
        return render_template(
            'cubiAdmin.html',
            collections_name=cubiDB.get_all_collections_names(),
            collections_ids=collections_ids,
            baseURL=baseURL
        )
    else:
        return redirect(baseURL)


# params = collection & id
@cubiItemShow_blueprint.route('/cubi/admin/item', methods=['GET'])
def show_item():
    if request.cookies.get('cubi_userID') == secret:
        collection = request.args.get('collection')
        id = request.args.get('id')
        item = cubiDB.get_item(collection, id)
        return item
    else:
        return redirect(baseURL)


@cubiItemCreate_blueprint.route('/cubi/admin/item/create', methods=['POST'])
def create_item():
    if request.cookies.get('cubi_userID') == secret:
        collection = request.form["collection_name"]
        cubiDB.duplicate_item(collection)
        return redirect('/cubi/admin')
    else:
        return redirect(baseURL)


@cubiItemUpdate_blueprint.route('/cubi/admin/item/update', methods=['POST'])
def update_item():
    if request.cookies.get('cubi_userID') == secret:
        json_data = json.loads(request.form["data"])
        collection = request.form["collection_name"]
        id = request.form["id"]
        del json_data["id"]
        cubiDB.update_item(collection, id, json_data)
        return redirect('/cubi/admin')
    else:
        return redirect(baseURL)


@cubiItemDelete_blueprint.route('/cubi/admin/item/delete', methods=['POST'])
def delete_item():
    if request.cookies.get('cubi_userID') == secret:
        collection = request.form["collection_name"]
        id = request.form["id"]
        cubiDB.remove_item(collection, id)
        return redirect('/cubi/admin')
    else:
        return redirect(baseURL)


@cubiCollectionRename_blueprint.route('/cubi/admin/collection/rename', methods=['POST'])
def rename_collection():
    if request.cookies.get('cubi_userID') == secret:
        old_collection_name = request.form["collection_name"]
        new_collection_name = request.form["new_collection_name"]
        cubiDB.rename_collection(old_collection_name, new_collection_name)
        return redirect('/cubi/admin')
    else:
        return redirect(baseURL)


@cubiCollectionDelete_blueprint.route('/cubi/admin/collection/delete', methods=['POST'])
def delete_collection():
    if request.cookies.get('cubi_userID') == secret:
        collection = request.form["collection_name"]
        cubiDB.remove_collection(collection)
        return redirect('/cubi/admin')
    else:
        return redirect(baseURL)


@cubiCollectionCreate_blueprint.route('/cubi/admin/collection/create', methods=['POST'])
def create_collection():
    if request.cookies.get('cubi_userID') == secret:
        collection_name = request.form["collection_name"]
        my_json = json.loads(request.form["data"])
        my_json['id'] = 0
        cubiDB.create_collection(collection_name, my_json)
        return redirect('/cubi/admin')
    else:
        return redirect(baseURL)
