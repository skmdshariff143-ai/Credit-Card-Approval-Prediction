// Client-side interactions for CreditGuard AI

document.addEventListener("DOMContentLoaded", function () {
    const unemployedSwitch = document.getElementById("unemployedSwitch");
    const empYearsGroup = document.getElementById("empYearsGroup");
    const occupationGroup = document.getElementById("occupationGroup");
    const empYearsInput = document.getElementById("empYearsInput");
    const occupationSelect = document.getElementById("occupationSelect");
    const predictionForm = document.getElementById("predictionForm");
    const loadingOverlay = document.getElementById("loadingOverlay");

    // Toggle employment input displays based on status
    function toggleEmploymentInputs() {
        if (unemployedSwitch && unemployedSwitch.checked) {
            if (empYearsGroup) empYearsGroup.style.display = "none";
            if (occupationGroup) occupationGroup.style.display = "none";
            if (empYearsInput) empYearsInput.value = "0";
            if (occupationSelect) occupationSelect.value = "Unknown";
        } else {
            if (empYearsGroup) empYearsGroup.style.display = "block";
            if (occupationGroup) occupationGroup.style.display = "block";
        }
    }

    if (unemployedSwitch) {
        toggleEmploymentInputs();
        unemployedSwitch.addEventListener("change", toggleEmploymentInputs);
    }

    // Spinner view on submit
    if (predictionForm) {
        predictionForm.addEventListener("submit", function () {
            if (predictionForm.checkValidity()) {
                if (loadingOverlay) {
                    loadingOverlay.classList.remove("d-none");
                }
            }
        });
    }
});
