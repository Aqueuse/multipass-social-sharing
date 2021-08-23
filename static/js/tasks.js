function taskSwitch(key, taskid) {
    let taskBlock = document.getElementById(key+"-"+taskid+"-task-block");
    let taskButton = document.getElementById(key+"-"+taskid+"-task-button");

    initFront(key, taskid);

    if (taskBlock.style.display === "block") {
        taskButton.innerHTML = "◁";
        taskBlock.style.display = "none";
        return;
    }
    if (taskBlock.style.display === "none") {
        taskButton.innerHTML = "▽";
        taskBlock.style.display = "block";
    }
}

function initFront(key, taskid) {
    let taskDay = document.getElementById(key+"-"+taskid+"-task-days");
    let taskMonth = document.getElementById(key+"-"+taskid+"-task-months");

    let valueDays = taskDay.value.split(",").map(x => x.trim());
    let valueMonths = taskMonth.value.split(",").map(x => x.trim());

    showPeriods(key, taskid);

    if (valueDays.length > 1) {
        for (let i = 0; i < valueDays.length; i++) {
            document.getElementById(key + "-" + taskid + "-span-" + valueDays[i]).style.backgroundColor = "lightskyblue";
        }
    }

    if (valueMonths.length > 1) {
        for (let i = 0; i < valueMonths.length; i++) {
            document.getElementById(key + "-" + taskid + "-span-" + valueMonths[i]).style.backgroundColor = "lightskyblue";
        }
    }
}

function showPeriods(key, taskid) {
    let repeat_chooser = document.getElementById(key+"-"+taskid+"-repetition");
    let choosen_repeat = repeat_chooser.options[repeat_chooser.selectedIndex].value;

    let divDays = document.getElementById(key+"-"+taskid+"-days");
    let divMonths = document.getElementById(key+"-"+taskid+"-months");

    switch (choosen_repeat) {
        case "daily":
            divDays.style.display = "none";
            divMonths.style.display = "none";
            break;
        case "weekly":
            divDays.style.display = "flex";
            divMonths.style.display = "none";
            break;
        case "monthly":
            divDays.style.display = "none";
            divMonths.style.display = "flex";
            break;
        case "custom":
            divDays.style.display = "flex";
            divMonths.style.display = "flex";
            break;
    }
}

function switchElement(key, taskid, period, element) {
    let roundSpan = document.getElementById(key+"-"+taskid+"-span-"+element).style.backgroundColor;
    let array = document.getElementById(key+"-"+taskid+"-task-"+period).value.split(",").map(x => x.trim());

    if (roundSpan === "lightsteelblue") {
        array = addElement(array, element);
        document.getElementById(key+"-"+taskid+"-span-"+element).style.backgroundColor = "lightskyblue";
        document.getElementById(key+"-"+taskid+"-task-"+period).value = array;
        return;
    }
    if (roundSpan === "lightskyblue") {
        array = removeElement(array, element);
        document.getElementById(key+"-"+taskid+"-span-"+element).style.backgroundColor = "lightsteelblue";
        document.getElementById(key+"-"+taskid+"-task-"+period).value = array;
    }
}

function addElement(array, element) {
    for (let i = 0; i < array.length; i++) {
        if (array[i] === element) {
            return;
        }
    }
    if (array.length === 1 && array[0] === "") array = [];
    array.push(element);
    return array;
}

function removeElement(array, element) {
    for (let i = 0; i < array.length; i++) {
        if (array[i] === element) {
            array.splice(i,i+1);
        }
    }
    return array;
}


function updateImagesList(key, taskid) {
    let files = document.getElementById(key+'-'+taskid+'-images-input').files;
    document.getElementById(key+'-'+taskid+'-images-list').innerText = "";
    let arrayFiles = Array.from(files);
    for (let i=0; i<arrayFiles.length; i++) {
        let div = document.createElement('div');
        div.innerText = arrayFiles[i].name;
        document.getElementById(key+'-'+taskid+'-images-list').appendChild(div);
    }
}

function removeImagesFromList(key, taskid) {
    document.getElementById(key+'-'+taskid+'-images-input').value = "";
    updateImagesList(key, taskid);
}