// LocalStorage
// Saved in JSON string format

function setItemLS(key, value) {
    localStorage.setItem(key, value);
}

function removeItemLS(key) {
    localStorage.removeItem(key);
}

// Logging Functionality
function consoleLogger(msg) {
    console.log(msg);
}

// DOM Manipulation
function showDateTime(id) {
    document.getElementById(id).innerHTML = Date();
}