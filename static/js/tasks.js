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


function showHideAllTasks(taskid) {
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

function activeSocialNetwork(taskid, socialNetwork) {
    document.getElementById(socialNetwork+"-"+taskid+"-ActivationFlag").setAttribute("value", "True");

    let socialTask = document.getElementById(socialNetwork+"-"+taskid+"-task-block");
    socialTask.style.display = "block";

    let taskExpanded = document.getElementById("task-"+taskid+"-expanded");
    taskExpanded.style.display = "block";

    let taskBlockParameters = document.getElementById(socialNetwork+"-"+taskid+"-parameters");
    taskBlockParameters.style.display = "block";

    let saveButton = document.getElementById(taskid+"-save-button");
    saveButton.style = "display: inline-block;";
    highlight(taskid);
}

function unactiveSocialNetwork(taskid, socialNetwork) {
    let socialTask = document.getElementById(socialNetwork+"-"+taskid+"-task-block");
    socialTask.style.display = "none";

    let saveButton = document.getElementById(taskid+"-save-button");

    let facebookTask = document.getElementById("facebook-"+taskid+"-task-block").style.display;
    let instagramTask = document.getElementById("instagram-"+taskid+"-task-block").style.display;
    let twitterTask = document.getElementById("twitter-"+taskid+"-task-block").style.display;

    document.getElementById(socialNetwork+"-"+taskid+"-ActivationFlag").setAttribute("value", "False");

    if (facebookTask == "none" && instagramTask == "none" && twitterTask == "none" ) {
        saveButton.style = "display: none;";
    }
    highlight(taskid);
}

let redColor = 255;

function highlight(taskid) {
  document.getElementById(taskid+"-save-button").className = 'highlight';
  setTimeout(function(){  document.getElementById(taskid+"-save-button").classList.remove("highlight"); }, 400);
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