/* ==========================================================================
   Premium Banking Portal Interactions & Chart.js Orchestrator
   Author: Senior Full Stack Architect
   ========================================================================== */

document.addEventListener('DOMContentLoaded', function () {
    // ----------------------------------------------------------------------
    // 1. Dark/Light Theme Switcher Logic
    // ----------------------------------------------------------------------
    const themeToggleBtn = document.getElementById('theme-toggle');
    const topLoader = document.querySelector('.top-loader');

    const triggerTopLoader = () => {
        if (topLoader) {
            topLoader.style.display = 'block';
            topLoader.style.width = '0%';
            topLoader.style.opacity = '1';
            let width = 0;
            const interval = setInterval(() => {
                width += 15;
                topLoader.style.width = `${width}%`;
                if (width >= 100) {
                    clearInterval(interval);
                    setTimeout(() => {
                        topLoader.style.opacity = '0';
                        setTimeout(() => {
                            topLoader.style.display = 'none';
                        }, 300);
                    }, 100);
                }
            }, 30);
        }
    };

    if (themeToggleBtn) {
        themeToggleBtn.addEventListener('click', () => {
            triggerTopLoader();
            const currentTheme = document.documentElement.getAttribute('data-bs-theme') || 'light';
            const newTheme = currentTheme === 'light' ? 'dark' : 'light';
            document.documentElement.setAttribute('data-bs-theme', newTheme);
            themeToggleBtn.innerHTML = newTheme === 'light' ? '<i class="bi bi-moon-stars"></i>' : '<i class="bi bi-sun"></i>';
            localStorage.setItem('theme', newTheme);
            
            // Refresh charts if they exist to match theme colors
            setTimeout(() => {
                if (window.adminCharts) {
                    window.adminCharts.forEach(chart => {
                        const textMain = getComputedStyle(document.documentElement).getPropertyValue('--text-main').trim();
                        const textMuted = getComputedStyle(document.documentElement).getPropertyValue('--text-muted').trim();
                        if (chart.options.scales && chart.options.scales.x) {
                            chart.options.scales.x.ticks.color = textMuted;
                        }
                        if (chart.options.scales && chart.options.scales.y) {
                            chart.options.scales.y.ticks.color = textMuted;
                        }
                        if (chart.options.plugins && chart.options.plugins.legend && chart.options.plugins.legend.labels) {
                            chart.options.plugins.legend.labels.color = textMain;
                        }
                        chart.update();
                    });
                }
            }, 100);
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
        triggerTopLoader();
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
                showToast("Please fill all required fields correctly before proceeding.", "danger");
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
                    <p class="mb-1"><strong>Gender:</strong> ${gender}</p>
                    <p class="mb-1"><strong>Age:</strong> ${age} Years</p>
                    <p class="mb-1"><strong>Marital Status:</strong> ${marital}</p>
                    <p class="mb-1"><strong>Children:</strong> ${children}</p>
                    <p class="mb-1"><strong>Education:</strong> ${education}</p>
                    <button type="button" class="btn btn-xs btn-outline-secondary mt-2 px-3 py-1 rounded-3" onclick="jumpToStep(0)"><i class="bi bi-pencil-square me-1"></i>Edit Profile</button>
                </div>
                <div class="col-md-4 border-end border-secondary-subtle">
                    <h5 class="text-primary mb-3"><i class="bi bi-briefcase-fill me-2"></i>Employment Details</h5>
                    <p class="mb-1"><strong>Sector:</strong> ${sector}</p>
                    <p class="mb-1"><strong>Occupation:</strong> ${occupation}</p>
                    <p class="mb-1"><strong>Experience:</strong> ${experience} Years</p>
                    <p class="mb-1"><strong>Income Source:</strong> ${source}</p>
                    <button type="button" class="btn btn-xs btn-outline-secondary mt-2 px-3 py-1 rounded-3" onclick="jumpToStep(1)"><i class="bi bi-pencil-square me-1"></i>Edit Employment</button>
                </div>
                <div class="col-md-4">
                    <h5 class="text-primary mb-3"><i class="bi bi-cash-coin me-2"></i>Financial Stats</h5>
                    <p class="mb-1"><strong>Gross Income:</strong> $${income}</p>
                    <p class="mb-1"><strong>Outstanding Debt:</strong> $${debt}</p>
                    <p class="mb-1"><strong>Requested Loan:</strong> $${loan}</p>
                    <p class="mb-1"><strong>Credit Rating:</strong> <span class="badge ${rating === 'Good' ? 'bg-success-subtle text-success border border-success' : rating === 'Average' ? 'bg-warning-subtle text-warning border border-warning' : 'bg-danger-subtle text-danger border border-danger'}">${rating}</span></p>
                    <p class="mb-1"><strong>Owns Asset (Car/Realty):</strong> ${car} / ${property}</p>
                    <button type="button" class="btn btn-xs btn-outline-secondary mt-2 px-3 py-1 rounded-3" onclick="jumpToStep(2)"><i class="bi bi-pencil-square me-1"></i>Edit Financials</button>
                </div>
            </div>
        `;
    };

    // ----------------------------------------------------------------------
    // 4. Admin Dashboard Chart.js rendering
    // ----------------------------------------------------------------------
    const statsContainer = document.getElementById('adminChartApproval');
    if (statsContainer) {
        window.adminCharts = [];
        const textMain = getComputedStyle(document.documentElement).getPropertyValue('--text-main').trim();
        const textMuted = getComputedStyle(document.documentElement).getPropertyValue('--text-muted').trim();

        fetch('/api/v1/admin/stats')
            .then(res => res.json())
            .then(data => {
                // 4.1 Pie Chart - Approval vs Rejection
                const approvedCount = parseInt(document.getElementById('statsApprovedCount')?.textContent || 0);
                const rejectedCount = parseInt(document.getElementById('statsRejectedCount')?.textContent || 0);
                
                const pieChart = new Chart(document.getElementById('adminChartApproval'), {
                    type: 'doughnut',
                    data: {
                        labels: ['Approved', 'Rejected'],
                        datasets: [{
                            data: [approvedCount, rejectedCount],
                            backgroundColor: ['#10b981', '#ef4444'],
                            borderWidth: 0,
                            hoverOffset: 4
                        }]
                    },
                    options: {
                        responsive: true,
                        cutout: '75%',
                        plugins: {
                            legend: { 
                                position: 'bottom', 
                                labels: { 
                                    color: textMain,
                                    font: { family: 'Poppins', size: 12 }
                                } 
                            }
                        }
                    }
                });
                window.adminCharts.push(pieChart);

                // Helper to build gradient
                const buildGradient = (ctx, colorStart, colorEnd) => {
                    const grad = ctx.createLinearGradient(0, 0, 0, 300);
                    grad.addColorStop(0, colorStart);
                    grad.addColorStop(1, colorEnd);
                    return grad;
                };

                // 4.2 Bar Chart - Income Distribution
                const ctxIncome = document.getElementById('adminChartIncome').getContext('2d');
                const gradIncome = buildGradient(ctxIncome, 'rgba(37, 99, 235, 0.85)', 'rgba(37, 99, 235, 0.25)');
                
                const incomeChart = new Chart(document.getElementById('adminChartIncome'), {
                    type: 'bar',
                    data: {
                        labels: data.income_labels,
                        datasets: [{
                            label: 'Application Count',
                            data: data.income_data,
                            backgroundColor: gradIncome,
                            borderColor: '#2563eb',
                            borderWidth: 1.5,
                            borderRadius: 8
                        }]
                    },
                    options: {
                        responsive: true,
                        plugins: { legend: { display: false } },
                        scales: {
                            y: { 
                                grid: { color: 'rgba(100,116,139,0.08)' }, 
                                ticks: { color: textMuted, font: { family: 'Poppins' } } 
                            },
                            x: { 
                                grid: { display: false }, 
                                ticks: { color: textMuted, font: { family: 'Poppins' } } 
                            }
                        }
                    }
                });
                window.adminCharts.push(incomeChart);

                // 4.3 Line Chart - Daily / Monthly Predictions Trend
                const ctxTrend = document.getElementById('adminChartTrend').getContext('2d');
                const gradTrend = buildGradient(ctxTrend, 'rgba(139, 92, 246, 0.4)', 'rgba(139, 92, 246, 0.02)');
                
                const trendChart = new Chart(document.getElementById('adminChartTrend'), {
                    type: 'line',
                    data: {
                        labels: data.trend_labels,
                        datasets: [{
                            label: 'Predictions Run',
                            data: data.trend_data,
                            borderColor: '#8b5cf6',
                            borderWidth: 3,
                            backgroundColor: gradTrend,
                            fill: true,
                            tension: 0.35,
                            pointBackgroundColor: '#8b5cf6',
                            pointRadius: 4
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: { legend: { display: false } },
                        scales: {
                            y: { 
                                grid: { color: 'rgba(100,116,139,0.08)' }, 
                                ticks: { color: textMuted, font: { family: 'Poppins' } } 
                            },
                            x: { 
                                grid: { display: false }, 
                                ticks: { color: textMuted, font: { family: 'Poppins' } } 
                            }
                        }
                    }
                });
                window.adminCharts.push(trendChart);

                // Trend Scale Toggle Listeners
                const btnDaily = document.getElementById('btnDailyTrend');
                const btnMonthly = document.getElementById('btnMonthlyTrend');
                if (btnDaily && btnMonthly) {
                    btnDaily.addEventListener('click', () => {
                        btnDaily.classList.add('active');
                        btnMonthly.classList.remove('active');
                        trendChart.data.labels = data.trend_labels;
                        trendChart.data.datasets[0].data = data.trend_data;
                        trendChart.data.datasets[0].label = 'Predictions Run (Daily)';
                        trendChart.update();
                    });
                    btnMonthly.addEventListener('click', () => {
                        btnMonthly.classList.add('active');
                        btnDaily.classList.remove('active');
                        trendChart.data.labels = data.monthly_labels || [];
                        trendChart.data.datasets[0].data = data.monthly_data || [];
                        trendChart.data.datasets[0].label = 'Predictions Run (Monthly)';
                        trendChart.update();
                    });
                }

                // 4.4 Bar Chart - Risk Level Distribution
                const riskChart = new Chart(document.getElementById('adminChartRisk'), {
                    type: 'bar',
                    data: {
                        labels: data.risk_labels,
                        datasets: [{
                            label: 'Applications',
                            data: data.risk_data,
                            backgroundColor: ['#10b981', '#3b82f6', '#f97316', '#ef4444'],
                            borderRadius: 8
                        }]
                    },
                    options: {
                        responsive: true,
                        plugins: { legend: { display: false } },
                        scales: {
                            y: { 
                                grid: { color: 'rgba(100,116,139,0.08)' }, 
                                ticks: { color: textMuted, font: { family: 'Poppins' } } 
                            },
                            x: { 
                                grid: { display: false }, 
                                ticks: { color: textMuted, font: { family: 'Poppins' } } 
                            }
                        }
                    }
                });
                window.adminCharts.push(riskChart);
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
        toast.className = `toast align-items-center text-white bg-${category} border-0 show mb-2 card-glass`;
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
            
            let overlay = document.getElementById('loading-overlay');
            if (!overlay) {
                overlay = document.createElement('div');
                overlay.id = 'loading-overlay';
                overlay.className = 'position-fixed top-0 start-0 w-100 h-100 d-flex flex-column align-items-center justify-content-center';
                overlay.style.cssText = 'background: rgba(15, 23, 42, 0.95); backdrop-filter: blur(16px); z-index: 9999; color: #fff; transition: opacity 0.3s ease;';
                overlay.innerHTML = `
                    <div class="spinner-border text-primary mb-4" role="status" style="width: 4rem; height: 4rem; border-width: 0.28em;">
                        <span class="visually-hidden">Loading...</span>
                    </div>
                    <h3 id="loading-status-text" class="text-uppercase tracking-wider fw-bold mb-2">Connecting...</h3>
                    <p id="loading-status-subtext" class="text-muted text-center px-4" style="max-width: 450px;">Initializing credit evaluation pipelines...</p>
                `;
                document.body.appendChild(overlay);
            }
            
            overlay.style.opacity = '1';
            overlay.classList.remove('d-none');
            
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
                    riskForm.submit();
                }
            }, 600);
        });
    }
});
