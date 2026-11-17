// Task 1 - Bill splitter
// Reads the three inputs, validates them, then shows the total with tip and the share per person.

function validateInputs(bill, tipRaw, peopleRaw) {
    var errors = [];   // list of { field, message }

    if (bill === "" || isNaN(Number(bill)) || Number(bill) <= 0) {
        errors.push({ field: "billAmount", message: "Total bill must be a number greater than 0." });
    }
    if (tipRaw === "") {
        errors.push({ field: "tipRate", message: "Please select a tip rate." });
    }
    var people = Number(peopleRaw);
    if (peopleRaw === "" || isNaN(people) || people < 1 || !Number.isInteger(people)) {
        errors.push({ field: "numPeople", message: "Number of people must be a whole number of at least 1." });
    }
    return errors;
}

function showErrors(errors) {
    var box = document.getElementById("errors");
    // clear the old highlighting
    ["billAmount", "tipRate", "numPeople"].forEach(function (id) {
        document.getElementById(id).classList.remove("invalid");
    });
    if (errors.length === 0) {
        box.innerHTML = "";
        box.style.display = "none";
        return;
    }
    var html = "<strong>Please fix the following:</strong><ul>";
    errors.forEach(function (e) {
        html += "<li>" + e.message + "</li>";
        document.getElementById(e.field).classList.add("invalid");
    });
    html += "</ul>";
    box.innerHTML = html;
    box.style.display = "block";
}

function calculateBill() {
    var bill   = document.getElementById("billAmount").value.trim();
    var tipRaw = document.getElementById("tipRate").value;
    var peopleRaw = document.getElementById("numPeople").value.trim();

    var errors = validateInputs(bill, tipRaw, peopleRaw);
    showErrors(errors);
    if (errors.length > 0) {
        document.getElementById("result").innerHTML = "";
        return;
    }

    var billNum = Number(bill);
    var tipPct  = Number(tipRaw);
    var people  = Number(peopleRaw);

    var tipAmount = billNum * tipPct / 100;     // <-- good place for a breakpoint
    var total     = billNum + tipAmount;
    var perPerson = total / people;

    document.getElementById("result").innerHTML =
        "<p>Tip amount: <strong>" + tipAmount.toFixed(2) + "</strong></p>" +
        "<p>Total with tip: <strong>" + total.toFixed(2) + "</strong></p>" +
        "<p>Each person pays: <strong>" + perPerson.toFixed(2) + "</strong></p>";
}

document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("calculate").onclick = calculateBill;
});
