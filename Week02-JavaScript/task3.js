// Task 3 - simple ToDo list (not persistent: refreshing the page clears it)

function addTodo() {
    var input = document.getElementById("todoText");
    var text = input.value.trim();
    var err = document.getElementById("todoError");

    if (text === "") {
        err.style.display = "block";
        err.innerHTML = "Please type something to do first.";
        input.classList.add("invalid");
        return;
    }
    err.style.display = "none";
    input.classList.remove("invalid");

    var li = document.createElement("li");
    var cb = document.createElement("input");
    cb.type = "checkbox";
    cb.addEventListener("change", function () {
        li.classList.toggle("done", cb.checked);      // tick = completed
        updateCount();
    });

    var span = document.createElement("span");
    span.textContent = text;                           // textContent => no HTML injection

    var del = document.createElement("button");
    del.textContent = "Delete";
    del.className = "danger";
    del.addEventListener("click", function () { li.remove(); updateCount(); });

    li.appendChild(cb);
    li.appendChild(span);
    li.appendChild(del);
    document.getElementById("todoList").appendChild(li);

    input.value = "";
    input.focus();
    updateCount();
}

function updateCount() {
    var all = document.querySelectorAll("#todoList li").length;
    var done = document.querySelectorAll("#todoList li.done").length;
    document.getElementById("count").textContent = done + " of " + all + " completed";
}

document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("addTodo").onclick = addTodo;
    document.getElementById("todoText").addEventListener("keydown", function (e) {
        if (e.key === "Enter") { addTodo(); }
    });
    updateCount();
});
