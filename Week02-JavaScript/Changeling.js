// Examples from the worksheet intro
function changeling(eid) {
    document.getElementById(eid).innerHTML = "<p>New text!</p>";
}

function setValue(ineid, num, outeid) {
    var input = Number(document.getElementById(ineid).value);   // Number() so it is not treated as text
    input += num;
    document.getElementById(outeid).innerHTML = input;
}

// Wiring up an event handler in the JS file keeps implementation details out of the HTML
window.addEventListener("DOMContentLoaded", function () {
    document.getElementById("calculate").onclick = function () {
        setValue("inputData", 10, "outputData");
    };
});
