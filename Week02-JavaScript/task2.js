// Task 2 - Bill splitter with menu items.
// The total bill is no longer typed in - it is the sum of all the items added.

var items = [];   // each item: { name: "Pizza", cost: 12.5 }

function renderItems() {
    var tbody = document.getElementById("itemRows");
    var html = "";
    items.forEach(function (it, i) {
        html += "<tr><td>" + escapeHtml(it.name) + "</td><td>" + it.cost.toFixed(2) + "</td>" +
                "<td><button class='danger' onclick='removeItem(" + i + ")'>X</button></td></tr>";
    });
    tbody.innerHTML = html || "<tr><td colspan='3'>No items yet.</td></tr>";
    document.getElementById("subtotal").innerHTML = sumItems().toFixed(2);
}

function escapeHtml(s) {
    return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

function sumItems() {
    return items.reduce(function (sum, it) { return sum + it.cost; }, 0);
}

function addItem() {
    var name = document.getElementById("itemName").value.trim();
    var costRaw = document.getElementById("itemCost").value.trim();
    var cost = Number(costRaw);
    var errors = [];

    if (name === "") { errors.push({ field: "itemName", message: "Enter the name of the item." }); }
    if (costRaw === "" || isNaN(cost) || cost <= 0) {
        errors.push({ field: "itemCost", message: "Cost must be a number greater than 0." });
    }
    showErrors(errors, ["itemName", "itemCost"], "itemErrors");
    if (errors.length) { return; }

    items.push({ name: name, cost: cost });
    document.getElementById("itemName").value = "";
    document.getElementById("itemCost").value = "";
    renderItems();
}

function removeItem(i) {
    items.splice(i, 1);
    renderItems();
}

function showErrors(errors, fieldIds, boxId) {
    var box = document.getElementById(boxId);
    fieldIds.forEach(function (id) { document.getElementById(id).classList.remove("invalid"); });
    if (errors.length === 0) { box.style.display = "none"; box.innerHTML = ""; return; }
    var html = "<strong>Please fix the following:</strong><ul>";
    errors.forEach(function (e) {
        html += "<li>" + e.message + "</li>";
        document.getElementById(e.field).classList.add("invalid");
    });
    box.innerHTML = html + "</ul>";
    box.style.display = "block";
}

function calculateBill() {
    var tipRaw = document.getElementById("tipRate").value;
    var peopleRaw = document.getElementById("numPeople").value.trim();
    var people = Number(peopleRaw);
    var errors = [];

    if (items.length === 0) { errors.push({ field: "itemName", message: "Add at least one menu item." }); }
    if (tipRaw === "") { errors.push({ field: "tipRate", message: "Please select a tip rate." }); }
    if (peopleRaw === "" || isNaN(people) || people < 1 || !Number.isInteger(people)) {
        errors.push({ field: "numPeople", message: "Number of people must be a whole number of at least 1." });
    }
    showErrors(errors, ["itemName", "tipRate", "numPeople"], "errors");
    if (errors.length) { document.getElementById("result").innerHTML = ""; return; }

    var bill = sumItems();                       // populated from the item list
    var tip = bill * Number(tipRaw) / 100;
    var total = bill + tip;
    var each = total / people;

    document.getElementById("result").innerHTML =
        "<div class='result'><p>Bill (sum of items): <strong>" + bill.toFixed(2) + "</strong></p>" +
        "<p>Tip: <strong>" + tip.toFixed(2) + "</strong></p>" +
        "<p>Total with tip: <strong>" + total.toFixed(2) + "</strong></p>" +
        "<p>Each person pays: <strong>" + each.toFixed(2) + "</strong></p></div>";
}

document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("addItem").onclick = addItem;
    document.getElementById("calculate").onclick = calculateBill;
    renderItems();
});
