// Client-side interactions for CreditGuard AI

document.addEventListener("DOMContentLoaded", function() {
    // Enable Bootstrap tooltips if any
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Enable custom form checks
    const form = document.querySelector(".needs-validation");
    const submitBtn = document.getElementById("submitBtn");
    if (form) {
        form.addEventListener("submit", function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            } else {
                if (submitBtn) {
                    submitBtn.disabled = true;
                    submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>Analyzing Credit Profile...';
                }
            }
            form.classList.add("was-validated");
        }, false);
    }
});
