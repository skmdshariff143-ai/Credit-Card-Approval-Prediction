// Client-side interactions for CreditGuard AI
// Implements form logic, validation, button states, and theme toggling helper

document.addEventListener("DOMContentLoaded", function() {
    // 1. Enable Bootstrap tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // 2. Auto-dismiss flash alerts/toasts after 5 seconds
    setTimeout(function() {
        const toasts = document.querySelectorAll('.toast');
        toasts.forEach(toastEl => {
            const bsToast = bootstrap.Toast.getInstance(toastEl);
            if (bsToast) {
                bsToast.hide();
            } else {
                toastEl.classList.remove('show');
            }
        });
    }, 5000);

    // 3. UI logic to coordinate "Unemployed/Retired" status with "Years Employed"
    const flagUnemployed = document.getElementById("flag_unemployed");
    const yearsEmployed = document.getElementById("years_employed");
    
    if (flagUnemployed && yearsEmployed) {
        const updateEmploymentState = () => {
            if (flagUnemployed.checked) {
                yearsEmployed.value = "0";
                yearsEmployed.setAttribute("readonly", "true");
                yearsEmployed.setAttribute("min", "0");
                yearsEmployed.setAttribute("max", "0");
                yearsEmployed.classList.add("bg-light-subtle");
            } else {
                yearsEmployed.removeAttribute("readonly");
                yearsEmployed.setAttribute("min", "0");
                yearsEmployed.setAttribute("max", "80");
                yearsEmployed.classList.remove("bg-light-subtle");
            }
        };
        
        // Run on load and on change
        updateEmploymentState();
        flagUnemployed.addEventListener("change", updateEmploymentState);
    }
    
    // 4. Form submission handler for premium validation styles and loading indicators
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
                    // Replace button text with a progress indicator
                    submitBtn.innerHTML = `
                        <span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                        Analyzing Risk Vector & Computing Local Explanations...
                    `;
                }
            }
            form.classList.add("was-validated");
        }, false);
    }
});
