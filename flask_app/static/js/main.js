// Client-side interactions for CreditGuard AI

document.addEventListener("DOMContentLoaded", function () {
    const unemployedSwitch = document.getElementById("unemployedSwitch");
    const empYearsGroup = document.getElementById("empYearsGroup");
    const occupationGroup = document.getElementById("occupationGroup");
    const empYearsInput = document.getElementById("empYearsInput");
    const occupationSelect = document.getElementById("occupationSelect");
    const predictionForm = document.getElementById("predictionForm");
    const loadingOverlay = document.getElementById("loadingOverlay");

    // Function to toggle employment inputs based on status
    function toggleEmploymentInputs() {
        if (unemployedSwitch.checked) {
            // Hide inputs
            empYearsGroup.style.display = "none";
            occupationGroup.style.display = "none";
            // Set values to defaults
            empYearsInput.value = "0";
            occupationSelect.value = "Unknown";
        } else {
            // Show inputs
            empYearsGroup.style.display = "block";
            occupationGroup.style.display = "block";
        }
    }

    // Initialize toggle state on page load
    if (unemployedSwitch) {
        toggleEmploymentInputs();
        unemployedSwitch.addEventListener("change", toggleEmploymentInputs);
    }

    // Show loading overlay when form is submitted successfully
    if (predictionForm) {
        predictionForm.addEventListener("submit", function (e) {
            // Verify if form is valid before showing loader (basic check)
            if (predictionForm.checkValidity()) {
                loadingOverlay.classList.remove("d-none");
            }
        });
    }
});
