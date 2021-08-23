function show_item(collection, id) {
    const url = '/cubi/admin/item?collection=' + collection + '&id=' + id;
    let request = new Request(url, {
        method: 'GET',
        headers: {
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest', //Necessary to work with request.is_ajax()
        },
    });

    fetch(request)
        .then(response => {
            return response.json();
        })
        .then(function (json) {
            generate_item_form(collection, id, json);
        });
}


function generate_item_form(collection_name, id, json_data) {
    document.getElementById("form-container").style.display = "inline-block";

    document.getElementById("collection").type = "hidden";
    document.getElementById("collection").value = collection_name;
    document.getElementById("id").value = id;
    document.getElementById("data").value = JSON.stringify(json_data);

    document.getElementById("collection-create-submit").style.display = "none";
    document.getElementById("item-update-submit").style.display = "inline-block";
    document.getElementById("item-delete-submit").style.display = "inline-block";

    editor.setValue(JSON.stringify(json_data, null, "\t"));
}

function generate_collection_form() {
    document.getElementById("form-container").style.display = "inline-block";

    document.getElementById("collection").type = "text"
    document.getElementById("collection").placeholder = "collection name";

    document.getElementById("collection-create-submit").style.display = "inline-block";
    document.getElementById("item-update-submit").style.display = "none";
    document.getElementById("item-delete-submit").style.display = "none";

    editor.setValue("{}");
}

function edit_field(field_id) {
    document.getElementById(field_id).removeAttribute("disabled");
}

function copy_json_data_to_form() {
    document.getElementById('data').value = editor.getValue();
}