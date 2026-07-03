/* ==========================================================================
   CreditGuard AI | Premium Core Frontend Controller
   Toggles, Drawer Navigation, Ripples, and 5-Step Form Wizard Engine
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {

  // 1. PAGE TRANSITION LOADER LIFECYCLE
  const loaderMask = document.getElementById('pageLoaderMask');
  if (loaderMask) {
    setTimeout(() => {
      loaderMask.classList.add('hidden');
    }, 250);
  }

  // 2. INITIALIZE SCROLL ANIMATIONS (AOS) & ICONS (Lucide)
  if (typeof aos !== 'undefined' || typeof AOS !== 'undefined') {
    AOS.init({
      duration: 800,
      easing: 'ease-out-cubic',
      once: true
    });
  }
  if (typeof lucide !== 'undefined') {
    lucide.createIcons();
  }

  // 3. GSAP INITIAL ANIMATION LOAD
  if (typeof gsap !== 'undefined') {
    gsap.from(".workspace-wrapper", {
      opacity: 0,
      y: 15,
      duration: 0.6,
      ease: "power2.out"
    });
  }

  // 4. DARK / LIGHT THEME PREFERENCE CONTROLLER
  const themeTogglerBtn = document.getElementById('themeTogglerBtn');
  const storedTheme = localStorage.getItem('theme') || 'dark';

  document.documentElement.setAttribute('data-theme', storedTheme);
  
  if (themeTogglerBtn) {
    const labelSpan = themeTogglerBtn.parentElement.querySelector('.theme-switch-label');
    if (labelSpan) {
      labelSpan.textContent = (storedTheme === 'dark') ? 'Dark Mode' : 'Light Mode';
    }

    themeTogglerBtn.addEventListener('click', () => {
      const active = document.documentElement.getAttribute('data-theme');
      const target = (active === 'dark') ? 'light' : 'dark';
      
      document.documentElement.setAttribute('data-theme', target);
      localStorage.setItem('theme', target);
      
      if (labelSpan) {
        labelSpan.textContent = (target === 'dark') ? 'Dark Mode' : 'Light Mode';
      }
    });
  }

  // 5. MOBILE DRAWER NAVIGATION MENU
  const menuOpenBtn = document.getElementById('mobileMenuOpen');
  const sidebarPanel = document.getElementById('sidebarPanel');
  const sidebarOverlay = document.getElementById('sidebarOverlay');

  if (menuOpenBtn && sidebarPanel && sidebarOverlay) {
    const toggleMenu = () => {
      sidebarPanel.classList.toggle('open');
      sidebarOverlay.classList.toggle('active');
    };

    menuOpenBtn.addEventListener('click', toggleMenu);
    sidebarOverlay.addEventListener('click', toggleMenu);
  }

  // 6. MULTI-STEP WIZARD ENGINE (5 Steps)
  const wizardForm = document.getElementById('wizardForm');
  if (wizardForm) {
    const panels = Array.from(wizardForm.querySelectorAll('.wizard-panel'));
    const stepNodes = Array.from(document.querySelectorAll('.wizard-step-node'));
    const fillBar = document.getElementById('wizardProgressFill');
    
    const backBtn = document.getElementById('wizardBack');
    const nextBtn = document.getElementById('wizardNext');
    const submitBtn = document.getElementById('wizardSubmit');
    
    let activeStep = 1;
    const maxSteps = 5;

    // Validate current panel entries
    const checkPanelInputs = (step) => {
      const panel = panels.find(p => parseInt(p.dataset.step) === step);
      if (!panel) return true;

      const fields = Array.from(panel.querySelectorAll('input, select'));
      let status = true;

      fields.forEach(field => {
        // Clear any old validation messages
        const formGroup = field.closest('.form-floating-premium') || field.closest('.form-group');
        if (formGroup) {
          const oldMsg = formGroup.querySelector('.form-error');
          if (oldMsg) oldMsg.remove();
        }

        if (field.hasAttribute('required') && !field.value.trim()) {
          status = false;
          appendError(field, 'This entry is required.');
        } else if (field.id === 'age_years' && field.value) {
          const age = parseFloat(field.value);
          if (isNaN(age) || age < 18 || age > 99) {
            status = false;
            appendError(field, 'Applicant age must be between 18 and 99 years.');
          }
        } else if (field.id === 'amt_income_total' && field.value) {
          const income = parseFloat(field.value);
          if (isNaN(income) || income <= 0) {
            status = false;
            appendError(field, 'Annual gross income must be a positive value.');
          }
        } else if (field.id === 'existing_debt' && field.value) {
          const debt = parseFloat(field.value);
          if (isNaN(debt) || debt < 0) {
            status = false;
            appendError(field, 'Debt outflow cannot be negative.');
          }
        } else if (field.id === 'loan_amount' && field.value) {
          const limit = parseFloat(field.value);
          if (isNaN(limit) || limit <= 0) {
            status = false;
            appendError(field, 'Requested limit must be a positive value.');
          }
        }
      });

      return status;
    };

    const appendError = (field, text) => {
      const formGroup = field.closest('.form-floating-premium') || field.closest('.form-group');
      if (formGroup) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'form-error animate-slide-up text-danger mt-1 fs-7';
        errorDiv.textContent = text;
        formGroup.appendChild(errorDiv);
      }
    };

    // Populates Step 4 Review summary blocks
    const compileSummaryDetails = () => {
      const summaryBox = document.getElementById('reviewSummary');
      if (!summaryBox) return;

      summaryBox.innerHTML = '';

      const mapping = [
        { label: 'Applicant Gender', id: 'code_gender' },
        { label: 'Applicant Age', id: 'age_years', suffix: ' Years' },
        { label: 'Marital Status', id: 'name_family_status' },
        { label: 'Children Count', id: 'cnt_children' },
        { label: 'Family Size', id: 'cnt_fam_members' },
        { label: 'Education Level', id: 'name_education_type' },
        { label: 'Housing Type', id: 'name_housing_type' },
        { label: 'Income Source', id: 'name_income_type' },
        { label: 'Occupation Sector', id: 'occupation_type' },
        { label: 'Experience duration', id: 'years_employed', suffix: ' Yrs' },
        { label: 'Gross Annual Income', id: 'amt_income_total', prefix: '$' },
        { label: 'Monthly Liabilities', id: 'existing_debt', prefix: '$' },
        { label: 'Requested Limit', id: 'loan_amount', prefix: '$' },
        { label: 'Bureau Repay History', id: 'credit_history' }
      ];

      mapping.forEach(item => {
        const field = document.getElementById(item.id);
        if (field) {
          let valText = '';
          if (field.tagName === 'SELECT') {
            valText = field.options[field.selectedIndex].text;
          } else {
            valText = field.value || 'N/A';
          }

          if (item.prefix && valText !== 'N/A') valText = item.prefix + valText;
          if (item.suffix && valText !== 'N/A') valText = valText + item.suffix;

          const block = document.createElement('div');
          block.className = 'col-sm-6 mb-3';
          block.innerHTML = `
            <div class="p-3 rounded bg-glass border border-light-subtle">
              <label class="d-block text-muted text-uppercase fs-9 fw-bold letter-spacing-1 mb-1">${item.label}</label>
              <span class="fs-6 fw-semibold text-primary-emphasis">${valText}</span>
            </div>
          `;
          summaryBox.appendChild(block);
        }
      });
    };

    // Transition wizard panels
    const displayActivePanel = () => {
      panels.forEach(p => {
        p.classList.toggle('active', parseInt(p.dataset.step) === activeStep);
      });

      // Fill bar
      if (fillBar) {
        const pct = ((activeStep - 1) / (maxSteps - 1)) * 100;
        fillBar.style.width = `${pct}%`;
      }

      // Steps indicator bubbles
      stepNodes.forEach(node => {
        const stepNum = parseInt(node.dataset.step);
        node.classList.toggle('active', stepNum === activeStep);
        node.classList.toggle('completed', stepNum < activeStep);
      });

      // Show/Hide navigation controls
      if (backBtn) {
        backBtn.style.visibility = (activeStep === 1) ? 'hidden' : 'visible';
      }

      if (activeStep === maxSteps) {
        if (nextBtn) nextBtn.style.display = 'none';
        if (submitBtn) submitBtn.style.display = 'inline-flex';
      } else {
        if (nextBtn) nextBtn.style.display = 'inline-flex';
        if (submitBtn) submitBtn.style.display = 'none';
      }

      if (activeStep === 4) {
        compileSummaryDetails();
      }
    };

    if (nextBtn) {
      nextBtn.addEventListener('click', () => {
        if (checkPanelInputs(activeStep)) {
          if (activeStep < maxSteps) {
            activeStep++;
            displayActivePanel();
            window.scrollTo({ top: 0, behavior: 'smooth' });
          }
        }
      });
    }

    if (backBtn) {
      backBtn.addEventListener('click', () => {
        if (activeStep > 1) {
          activeStep--;
          displayActivePanel();
          window.scrollTo({ top: 0, behavior: 'smooth' });
        }
      });
    }

    // Step indicators clickable navigations
    stepNodes.forEach(node => {
      node.addEventListener('click', () => {
        const targetStep = parseInt(node.dataset.step);
        if (targetStep < activeStep) {
          activeStep = targetStep;
          displayActivePanel();
        } else if (targetStep > activeStep) {
          // Validate intermediate steps
          let canGo = true;
          for (let s = activeStep; s < targetStep; s++) {
            if (!checkPanelInputs(s)) {
              canGo = false;
              break;
            }
          }
          if (canGo) {
            activeStep = targetStep;
            displayActivePanel();
          }
        }
      });
    });

    displayActivePanel();
  }

});
