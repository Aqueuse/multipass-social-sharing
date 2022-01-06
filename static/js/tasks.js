function showHideAllTasks(taskid) {
    console.log("showHideAllTasks");
    let taskBlock = document.getElementById("task-"+taskid+"-expanded");
    let taskButton = document.getElementById("task-"+taskid+"-button");
    let taskLogo = document.getElementById("resume-social-networks-icons");

    initFront(taskid);

    if (taskBlock.style.display === "block") {
        taskButton.innerHTML = "◁";
        taskBlock.style.display = "none";
        taskLogo.style.display = "block";
        return;
    }
    if (taskBlock.style.display === "none") {
        taskButton.innerHTML = "▽";
        taskBlock.style.display = "block";
        taskLogo.style.display = "none";
    }
}

function showHideThisTask(taskid, socialNetwork) {
    let socialTask = document.getElementById(socialNetwork+"-"+taskid+"-parameters");

    if (socialTask.style.display === "block") {
        socialTask.style.display = "none";
        return;
    }
    if (socialTask.style.display === "none") {
        socialTask.style.display = "block";
    }
}

function initFront(taskid) {
    let taskDay = document.getElementById(taskid+"-task-days");
    let taskMonth = document.getElementById(taskid+"-task-months");

    let valueDays = taskDay.value.split(",").map(x => x.trim());
    let valueMonths = taskMonth.value.split(",").map(x => x.trim());

    showPeriods(taskid);

    if (valueDays.length > 1) {
        for (let i = 0; i < valueDays.length; i++) {
            document.getElementById(taskid + "-span-" + valueDays[i]).style.backgroundColor = "lightskyblue";
        }
    }

    if (valueMonths.length > 1) {
        for (let i = 0; i < valueMonths.length; i++) {
            document.getElementById(taskid + "-span-" + valueMonths[i]).style.backgroundColor = "lightskyblue";
        }
    }
}

function editTaskname(taskid) {
    let taskname_a = document.getElementById("task-"+taskid+"-name-a");
    let taskname_area = document.getElementById("task-"+taskid+"-name-area");

    if (taskname_a.style.display === "block") {
        taskname_a.style.display = "none";
        taskname_area.style.display = "block";
        // change button image to a V (to validdate)
        return;
    }

    if (taskname_a.style.display === "none") {
        taskname_a.innerText = taskname_area.value;
        taskname_a.style.display = "block";
        taskname_area.style.display = "none";
        // change button image to a pen (to edit)
    }
}

function showPeriods(taskid) {
    let repeat_chooser = document.getElementById(taskid+"-repetition");
    let choosen_repeat = repeat_chooser.options[repeat_chooser.selectedIndex].value;

    let divDays = document.getElementById(taskid+"-days");
    let divMonths = document.getElementById(taskid+"-months");

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

function switchElement(taskid, period, element) {
    let roundSpan = document.getElementById(taskid+"-span-"+element).style.backgroundColor;
    let array = document.getElementById(taskid+"-task-"+period).value.split(",").map(x => x.trim());

    if (roundSpan === "lightsteelblue") {
        array = addElement(array, element);
        document.getElementById(taskid+"-span-"+element).style.backgroundColor = "lightskyblue";
        document.getElementById(taskid+"-task-"+period).value = array;
        return;
    }
    if (roundSpan === "lightskyblue") {
        array = removeElement(array, element);
        document.getElementById(taskid+"-span-"+element).style.backgroundColor = "lightsteelblue";
        document.getElementById(taskid+"-task-"+period).value = array;
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


function updateImagesList(socialNetwork, taskid) {
    let files = document.getElementById(socialNetwork+'-'+taskid+'-images-input').files;
    document.getElementById(socialNetwork+'-'+taskid+'-images-list').innerText = "";
    let arrayFiles = Array.from(files);
    for (let i=0; i<arrayFiles.length; i++) {
        let div = document.createElement('div');
        div.innerText = arrayFiles[i].name;
        document.getElementById(socialNetwork+'-'+taskid+'-images-list').appendChild(div);
    }
}

function removeImagesFromList(socialNetwork, taskid) {
    document.getElementById(socialNetwork+'-'+taskid+'-images-input').value = "";
    updateImagesList(key, taskid);
}