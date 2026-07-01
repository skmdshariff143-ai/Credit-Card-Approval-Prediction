/* ==========================================================================
   Premium Banking Portal Interactions & Chart.js Orchestrator
   Author: Senior Full Stack Architect
   ========================================================================== */

document.addEventListener('DOMContentLoaded', function () {
    // ----------------------------------------------------------------------
    // 1. Dark/Light Theme Switcher Logic
    // ----------------------------------------------------------------------
    const themeToggleBtn = document.getElementById('theme-toggle');
    if (themeToggleBtn) {
        themeToggleBtn.addEventListener('click', () => {
            const currentTheme = document.documentElement.getAttribute('data-bs-theme') || 'light';
            const newTheme = currentTheme === 'light' ? 'dark' : 'light';
            document.documentElement.setAttribute('data-bs-theme', newTheme);
            themeToggleBtn.innerHTML = newTheme === 'light' ? '<i class="bi bi-moon-stars"></i>' : '<i class="bi bi-sun"></i>';
            localStorage.setItem('theme', newTheme);
        });
    }

    // Set saved theme on load
    const savedTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-bs-theme', savedTheme);
    if (themeToggleBtn) {
        themeToggleBtn.innerHTML = savedTheme === 'light' ? '<i class="bi bi-moon-stars"></i>' : '<i class="bi bi-sun"></i>';
    }

    // ----------------------------------------------------------------------
    // 2. Unemployment Toggle Logic
    // ----------------------------------------------------------------------
    const unemployedCheck = document.getElementById('flag_unemployed');
    const yearsEmployedInput = document.getElementById('years_employed');
    const occupationSelect = document.getElementById('occupation_type');

    if (unemployedCheck && yearsEmployedInput) {
        const toggleEmploymentInputs = () => {
            if (unemployedCheck.checked) {
                yearsEmployedInput.value = '0';
                yearsEmployedInput.setAttribute('readonly', 'true');
                yearsEmployedInput.classList.add('bg-secondary-subtle');
                if (occupationSelect) {
                    occupationSelect.value = 'Unknown';
                    occupationSelect.setAttribute('disabled', 'true');
                }
            } else {
                yearsEmployedInput.removeAttribute('readonly');
                yearsEmployedInput.classList.remove('bg-secondary-subtle');
                if (occupationSelect) {
                    occupationSelect.removeAttribute('disabled');
                }
            }
        };

        unemployedCheck.addEventListener('change', toggleEmploymentInputs);
        toggleEmploymentInputs(); // trigger initial state
    }

    // ----------------------------------------------------------------------
    // 3. Multi-Step Form Wizard Navigation
    // ----------------------------------------------------------------------
    const wizardSteps = document.querySelectorAll('.wizard-step');
    const nextButtons = document.querySelectorAll('.btn-next');
    const prevButtons = document.querySelectorAll('.btn-prev');
    const stepNodes = document.querySelectorAll('.step-node');
    const stepProgress = document.querySelector('.step-progress-bar');
    let currentStepIdx = 0;

    const updateStepUI = () => {
        // Update Step visibility
        wizardSteps.forEach((step, idx) => {
            if (idx === currentStepIdx) {
                step.classList.add('active');
            } else {
                step.classList.remove('active');
            }
        });

        // Update Node Classes
        stepNodes.forEach((node, idx) => {
            if (idx < currentStepIdx) {
                node.className = 'step-node completed';
                node.innerHTML = '<i class="bi bi-check-lg"></i>';
            } else if (idx === currentStepIdx) {
                node.className = 'step-node active';
                node.innerHTML = idx + 1;
            } else {
                node.className = 'step-node';
                node.innerHTML = idx + 1;
            }
        });

        // Update progress bar length
        if (stepProgress) {
            const progressPct = (currentStepIdx / (wizardSteps.length - 1)) * 100;
            stepProgress.style.width = `${progressPct}%`;
        }

        // Generate review panel contents if entering step 4
        if (currentStepIdx === 3) {
            generateReviewPanel();
        }
    };

    const validateStep = (stepIdx) => {
        let isValid = true;
        const currentStepEl = wizardSteps[stepIdx];
        if (!currentStepEl) return true;

        const inputs = currentStepEl.querySelectorAll('input, select');
        inputs.forEach(input => {
            // Check HTML5 validations
            if (input.hasAttribute('required') && !input.value.trim()) {
                input.classList.add('is-invalid');
                isValid = false;
            } else if (input.type === 'number' || input.classList.contains('form-control')) {
                // Bounds validation check
                const val = parseFloat(input.value);
                const min = parseFloat(input.getAttribute('min'));
                const max = parseFloat(input.getAttribute('max'));
                
                if (!isNaN(val)) {
                    if (!isNaN(min) && val < min) {
                        input.classList.add('is-invalid');
                        isValid = false;
                    } else if (!isNaN(max) && val > max) {
                        input.classList.add('is-invalid');
                        isValid = false;
                    } else {
                        input.classList.remove('is-invalid');
                    }
                }
            } else {
                input.classList.remove('is-invalid');
            }
        });
        return isValid;
    };

    nextButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            if (validateStep(currentStepIdx)) {
                if (currentStepIdx < wizardSteps.length - 1) {
                    currentStepIdx++;
                    updateStepUI();
                }
            } else {
                // Trigger toast or message
                showToast("Please fill all required inputs correctly before proceeding.", "danger");
            }
        });
    });

    prevButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            if (currentStepIdx > 0) {
                currentStepIdx--;
                updateStepUI();
            }
        });
    });

    // Edit button hooks from review screen
    window.jumpToStep = (stepIdx) => {
        if (stepIdx >= 0 && stepIdx < wizardSteps.length) {
            currentStepIdx = stepIdx;
            updateStepUI();
        }
    };

    // Review Panel content builder
    const generateReviewPanel = () => {
        const reviewContainer = document.getElementById('review-summary-panel');
        if (!reviewContainer) return;

        // Scrape values
        const gender = document.getElementById('code_gender')?.value === 'M' ? 'Male' : 'Female';
        const age = document.getElementById('age_years')?.value;
        const marital = document.getElementById('name_family_status')?.value;
        const children = document.getElementById('cnt_children')?.value;
        const education = document.getElementById('name_education_type')?.value;
        
        const occupation = document.getElementById('occupation_type')?.value;
        const sector = document.getElementById('name_income_type')?.value;
        const experience = document.getElementById('years_employed')?.value;
        const source = document.getElementById('income_source')?.value;

        const income = parseFloat(document.getElementById('amt_income_total')?.value || 0).toLocaleString();
        const debt = parseFloat(document.getElementById('existing_debt')?.value || 0).toLocaleString();
        const loan = parseFloat(document.getElementById('loan_amount')?.value || 0).toLocaleString();
        const rating = document.getElementById('credit_history')?.value;
        const car = document.getElementById('flag_own_car')?.value === 'Y' ? 'Yes' : 'No';
        const property = document.getElementById('flag_own_realty')?.value === 'Y' ? 'Yes' : 'No';

        reviewContainer.innerHTML = `
            <div class="row g-4 text-start">
                <div class="col-md-4 border-end border-secondary-subtle">
                    <h5 class="text-primary mb-3"><i class="bi bi-person-fill me-2"></i>Personal Profile</h5>
                    <p><strong>Gender:</strong> ${gender}</p>
                    <p><strong>Age:</strong> ${age} Years</p>
                    <p><strong>Marital Status:</strong> ${marital}</p>
                    <p><strong>Children:</strong> ${children}</p>
                    <p><strong>Education:</strong> ${education}</p>
                    <button type="button" class="btn btn-sm btn-outline-secondary mt-2" onclick="jumpToStep(0)"><i class="bi bi-pencil-square me-1"></i>Edit Profile</button>
                </div>
                <div class="col-md-4 border-end border-secondary-subtle">
                    <h5 class="text-primary mb-3"><i class="bi bi-briefcase-fill me-2"></i>Employment Details</h5>
                    <p><strong>Sector:</strong> ${sector}</p>
                    <p><strong>Occupation:</strong> ${occupation}</p>
                    <p><strong>Experience:</strong> ${experience} Years</p>
                    <p><strong>Income Source:</strong> ${source}</p>
                    <button type="button" class="btn btn-sm btn-outline-secondary mt-2" onclick="jumpToStep(1)"><i class="bi bi-pencil-square me-1"></i>Edit Employment</button>
                </div>
                <div class="col-md-4">
                    <h5 class="text-primary mb-3"><i class="bi bi-cash-coin me-2"></i>Financial Stats</h5>
                    <p><strong>Gross Income:</strong> $${income}</p>
                    <p><strong>Outstanding Debt:</strong> $${debt}</p>
                    <p><strong>Requested Loan:</strong> $${loan}</p>
                    <p><strong>Credit Bureau Rating:</strong> <span class="badge ${rating === 'Good' ? 'bg-success' : rating === 'Average' ? 'bg-warning text-dark' : 'bg-danger'}">${rating}</span></p>
                    <p><strong>Owns Asset (Car/Realty):</strong> ${car} / ${property}</p>
                    <button type="button" class="btn btn-sm btn-outline-secondary mt-2" onclick="jumpToStep(2)"><i class="bi bi-pencil-square me-1"></i>Edit Financials</button>
                </div>
            </div>
        `;
    };

    // ----------------------------------------------------------------------
    // 4. Admin Dashboard Chart.js rendering
    // ----------------------------------------------------------------------
    const statsContainer = document.getElementById('adminChartApproval');
    if (statsContainer) {
        fetch('/api/v1/admin/stats')
            .then(res => res.json())
            .then(data => {
                // 4.1 Pie Chart - Approval vs Rejection
                const approvedCount = parseInt(document.getElementById('statsApprovedCount')?.textContent || 0);
                const rejectedCount = parseInt(document.getElementById('statsRejectedCount')?.textContent || 0);
                
                new Chart(document.getElementById('adminChartApproval'), {
                    type: 'doughnut',
                    data: {
                        labels: ['Approved', 'Rejected'],
                        datasets: [{
                            data: [approvedCount, rejectedCount],
                            backgroundColor: ['#198754', '#dc3545'],
                            borderWidth: 0
                        }]
                    },
                    options: {
                        responsive: true,
                        plugins: {
                            legend: { position: 'bottom', labels: { color: getComputedStyle(document.documentElement).getPropertyValue('--text-main') } }
                        }
                    }
                });

                // 4.2 Bar Chart - Income Distribution
                new Chart(document.getElementById('adminChartIncome'), {
                    type: 'bar',
                    data: {
                        labels: data.income_labels,
                        datasets: [{
                            label: 'Application Count',
                            data: data.income_data,
                            backgroundColor: '#0d6efd',
                            borderRadius: 6
                        }]
                    },
                    options: {
                        responsive: true,
                        plugins: {
                            legend: { display: false }
                        },
                        scales: {
                            y: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: getComputedStyle(document.documentElement).getPropertyValue('--text-muted') } },
                            x: { grid: { display: false }, ticks: { color: getComputedStyle(document.documentElement).getPropertyValue('--text-muted') } }
                        }
                    }
                });

                // 4.3 Line Chart - Daily Predictions Trend
                new Chart(document.getElementById('adminChartTrend'), {
                    type: 'line',
                    data: {
                        labels: data.trend_labels,
                        datasets: [{
                            label: 'Predictions Run',
                            data: data.trend_data,
                            borderColor: '#fd7e14',
                            backgroundColor: 'rgba(253, 126, 20, 0.1)',
                            fill: true,
                            tension: 0.3
                        }]
                    },
                    options: {
                        responsive: true,
                        plugins: { legend: { display: false } },
                        scales: {
                            y: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: getComputedStyle(document.documentElement).getPropertyValue('--text-muted') } },
                            x: { grid: { display: false }, ticks: { color: getComputedStyle(document.documentElement).getPropertyValue('--text-muted') } }
                        }
                    }
                });

                // 4.4 Bar Chart - Risk Level Distribution
                new Chart(document.getElementById('adminChartRisk'), {
                    type: 'bar',
                    data: {
                        labels: data.risk_labels,
                        datasets: [{
                            label: 'Applications',
                            data: data.risk_data,
                            backgroundColor: ['#10b981', '#3b82f6', '#f97316', '#ef4444'],
                            borderRadius: 6
                        }]
                    },
                    options: {
                        responsive: true,
                        plugins: { legend: { display: false } },
                        scales: {
                            y: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: getComputedStyle(document.documentElement).getPropertyValue('--text-muted') } },
                            x: { grid: { display: false }, ticks: { color: getComputedStyle(document.documentElement).getPropertyValue('--text-muted') } }
                        }
                    }
                });
            })
            .catch(err => console.error("Stats fetching failure: ", err));
    }

    // ----------------------------------------------------------------------
    // 5. Toast Notifications Helper
    // ----------------------------------------------------------------------
    const showToast = (message, category = "info") => {
        const container = document.getElementById('toast-container');
        if (!container) return;

        const toast = document.createElement('div');
        toast.className = `toast align-items-center text-white bg-${category} border-0 show mb-2`;
        toast.setAttribute('role', 'alert');
        toast.setAttribute('aria-live', 'assertive');
        toast.setAttribute('aria-atomic', 'true');

        toast.innerHTML = `
            <div class="d-flex">
                <div class="toast-body">
                    <i class="bi bi-info-circle-fill me-2"></i>${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
        `;

        container.appendChild(toast);
        setTimeout(() => {
            toast.remove();
        }, 5000);
    };

    // ----------------------------------------------------------------------
    // 6. Export and Share Utilities
    // ----------------------------------------------------------------------
    const shareReportBtn = document.getElementById('btn-share-report');
    if (shareReportBtn) {
        shareReportBtn.addEventListener('click', () => {
            const shareUrl = window.location.href;
            if (navigator.share) {
                navigator.share({
                    title: 'Credit Score Assessment Report',
                    text: 'View details of applicant risk assessment logs.',
                    url: shareUrl,
                }).catch(err => console.log(err));
            } else {
                // Clipboard fallback
                navigator.clipboard.writeText(shareUrl).then(() => {
                    showToast("Report URL successfully copied to clipboard!", "success");
                });
            }
        });
    }

    const printReportBtn = document.getElementById('btn-print-report');
    if (printReportBtn) {
        printReportBtn.addEventListener('click', () => {
            window.print();
        });
    }

    // ----------------------------------------------------------------------
    // 7. Form Submission Loading Screen Orchestration
    // ----------------------------------------------------------------------
    const riskForm = document.getElementById('wizard-risk-form');
    if (riskForm) {
        riskForm.addEventListener('submit', function (e) {
            e.preventDefault();
            
            // 1. Create and inject the loading overlay HTML dynamically if not exists
            let overlay = document.getElementById('loading-overlay');
            if (!overlay) {
                overlay = document.createElement('div');
                overlay.id = 'loading-overlay';
                overlay.className = 'position-fixed top-0 start-0 w-100 h-100 d-flex flex-column align-items-center justify-content-center';
                overlay.style.cssText = 'background: rgba(15, 23, 42, 0.9); backdrop-filter: blur(12px); z-index: 9999; color: #fff; transition: opacity 0.3s ease;';
                overlay.innerHTML = `
                    <div class="spinner-border text-primary mb-4" role="status" style="width: 4rem; height: 4rem;">
                        <span class="visually-hidden">Loading...</span>
                    </div>
                    <h3 id="loading-status-text" class="text-uppercase tracking-wider fw-bold mb-2">Connecting...</h3>
                    <p id="loading-status-subtext" class="text-muted text-center px-4" style="max-width: 450px;">Initializing credit evaluation pipelines...</p>
                `;
                document.body.appendChild(overlay);
            }
            
            overlay.style.opacity = '1';
            overlay.classList.remove('d-none');
            
            // 2. Cycle messages
            const statusText = document.getElementById('loading-status-text');
            const statusSubtext = document.getElementById('loading-status-subtext');
            
            const steps = [
                { text: "Connecting...", sub: "Establishing secure link to CreditGuard decision engine..." },
                { text: "Loading model...", sub: "Fetching Logistic Regression weights and validation templates..." },
                { text: "Preparing prediction...", sub: "Transforming socio-demographic features and scaling financials..." },
                { text: "Application Ready", sub: "Finalizing risk evaluation scores..." }
            ];
            
            let currentStep = 0;
            const interval = setInterval(() => {
                currentStep++;
                if (currentStep < steps.length) {
                    statusText.textContent = steps[currentStep].text;
                    statusSubtext.textContent = steps[currentStep].sub;
                } else {
                    clearInterval(interval);
                    // Submit the form actually
                    riskForm.submit();
                }
            }, 600); // 600ms per stage, total ~2.4s of beautiful premium loading animation
        });
    }
});
