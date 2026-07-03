/* ==========================================================================
   CreditGuard AI | Premium Core Frontend Controller
   Toggles, Drawer Navigation, Ripples, and 5-Step Form Wizard Engine
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {
  
  // 1. PAGE TRANSITION LOADER LIFECYCLE
  const loader = document.getElementById('pageLoader');
  if (loader) {
    setTimeout(() => {
      loader.classList.add('hidden');
    }, 180);
  }

  // 2. MODERN LIGHT/DARK THEME TOGGLE
  const themeSwitchControl = document.getElementById('themeSwitchControl');
  const themeTogglerBtn = document.getElementById('themeTogglerBtn');
  const activeTheme = localStorage.getItem('theme') || 'dark';

  document.documentElement.setAttribute('data-theme', activeTheme);
  
  // Align toggle label if exist
  if (themeTogglerBtn) {
    const label = themeTogglerBtn.querySelector('.theme-label-text');
    if (label) {
      label.textContent = (activeTheme === 'dark') ? 'Dark Mode' : 'Light Mode';
    }
  }

  if (themeSwitchControl) {
    themeSwitchControl.addEventListener('click', () => {
      const current = document.documentElement.getAttribute('data-theme');
      const target = (current === 'dark') ? 'light' : 'dark';
      
      document.documentElement.setAttribute('data-theme', target);
      localStorage.setItem('theme', target);

      if (themeTogglerBtn) {
        const label = themeTogglerBtn.querySelector('.theme-label-text');
        if (label) {
          label.textContent = (target === 'dark') ? 'Dark Mode' : 'Light Mode';
        }
      }
    });
  }

  // 3. MOBILE SIDEBAR DRAWER INTERACTIONS
  const sidebarToggle = document.getElementById('sidebarToggle');
  const sidebarDrawer = document.getElementById('sidebarDrawer');
  const sidebarBackdrop = document.getElementById('sidebarBackdrop');

  if (sidebarToggle && sidebarDrawer && sidebarBackdrop) {
    const toggleSidebar = () => {
      sidebarDrawer.classList.toggle('open');
      sidebarBackdrop.classList.toggle('active');
    };

    sidebarToggle.addEventListener('click', toggleSidebar);
    sidebarBackdrop.addEventListener('click', toggleSidebar);

    // Close on navigation
    const navLinks = sidebarDrawer.querySelectorAll('.menu-item');
    navLinks.forEach(link => {
      link.addEventListener('click', () => {
        sidebarDrawer.classList.remove('open');
        sidebarBackdrop.classList.remove('active');
      });
    });
  }

  // 4. MULTI-STEP WIZARD ENGINE (5 Steps)
  const wizardForm = document.getElementById('wizardForm');
  if (wizardForm) {
    const panels = Array.from(wizardForm.querySelectorAll('.wizard-step-panel'));
    const indicators = Array.from(document.querySelectorAll('.timeline-step'));
    const fill = document.getElementById('wizardProgressFill');
    
    const backBtn = document.getElementById('wizardBack');
    const nextBtn = document.getElementById('wizardNext');
    const submitBtn = document.getElementById('wizardSubmit');
    
    let currentStep = 1;
    const totalSteps = 5;

    // Validate active step fields
    const validateStep = (step) => {
      const activePanel = panels.find(p => parseInt(p.dataset.step) === step);
      if (!activePanel) return true;

      const inputs = Array.from(activePanel.querySelectorAll('input, select'));
      let isValid = true;

      inputs.forEach(input => {
        // Clear any old validation messages
        const parent = input.closest('.form-group');
        if (parent) {
          const oldMsg = parent.querySelector('.form-error');
          if (oldMsg) oldMsg.remove();
        }

        // Run verification checks
        if (input.hasAttribute('required') && !input.value.trim()) {
          isValid = false;
          showErrorMsg(input, 'This entry is required.');
        } else if (input.id === 'age_years' && input.value) {
          const age = parseFloat(input.value);
          if (isNaN(age) || age < 18 || age > 99) {
            isValid = false;
            showErrorMsg(input, 'Applicant age must be between 18 and 99 years.');
          }
        } else if (input.id === 'amt_income_total' && input.value) {
          const income = parseFloat(input.value);
          if (isNaN(income) || income <= 0) {
            isValid = false;
            showErrorMsg(input, 'Annual gross income must be a positive value.');
          }
        } else if (input.id === 'existing_debt' && input.value) {
          const debt = parseFloat(input.value);
          if (isNaN(debt) || debt < 0) {
            isValid = false;
            showErrorMsg(input, 'Debt payments cannot be negative.');
          }
        } else if (input.id === 'loan_amount' && input.value) {
          const limit = parseFloat(input.value);
          if (isNaN(limit) || limit <= 0) {
            isValid = false;
            showErrorMsg(input, 'Credit limit must be a positive value.');
          }
        }
      });

      return isValid;
    };

    const showErrorMsg = (input, msg) => {
      const parent = input.closest('.form-group');
      if (parent) {
        const err = document.createElement('div');
        err.className = 'form-error animate-slide-up';
        err.textContent = msg;
        parent.appendChild(err);
      }
    };

    // Extract entries to populate Step 4 (Review) summary grid
    const populateReviewSummary = () => {
      const summaryGrid = document.getElementById('reviewSummary');
      if (!summaryGrid) return;
      
      summaryGrid.innerHTML = '';
      
      const elementsMap = [
        { label: 'Gender', id: 'code_gender' },
        { label: 'Age', id: 'age_years', suffix: ' Years' },
        { label: 'Marital Status', id: 'name_family_status' },
        { label: 'Children', id: 'cnt_children' },
        { label: 'Family Members', id: 'cnt_fam_members' },
        { label: 'Education', id: 'name_education_type' },
        { label: 'Housing Type', id: 'name_housing_type' },
        { label: 'Income Category', id: 'name_income_type' },
        { label: 'Occupation Sector', id: 'occupation_type' },
        { label: 'Employment Duration', id: 'years_employed', suffix: ' Yrs' },
        { label: 'Gross Annual Income', id: 'amt_income_total', prefix: '$' },
        { label: 'Monthly Debt Outflow', id: 'existing_debt', prefix: '$' },
        { label: 'Requested Limit', id: 'loan_amount', prefix: '$' },
        { label: 'Credit Rating', id: 'credit_history' }
      ];

      elementsMap.forEach(field => {
        const input = document.getElementById(field.id);
        if (input) {
          let text = '';
          if (input.tagName === 'SELECT') {
            text = input.options[input.selectedIndex].text;
          } else {
            text = input.value || 'N/A';
          }
          
          if (field.prefix && text !== 'N/A') text = field.prefix + text;
          if (field.suffix && text !== 'N/A') text = text + field.suffix;

          const block = document.createElement('div');
          block.className = 'wizard-summary-item';
          block.innerHTML = `
            <label>${field.label}</label>
            <span>${text}</span>
          `;
          summaryGrid.appendChild(block);
        }
      });
    };

    // Change step view layout
    const transitionStep = () => {
      panels.forEach(panel => {
        panel.classList.toggle('active', parseInt(panel.dataset.step) === currentStep);
      });

      // Fill line length
      if (fill) {
        const pct = ((currentStep - 1) / (totalSteps - 1)) * 100;
        fill.style.width = `${pct}%`;
      }

      // Step indicators
      indicators.forEach(ind => {
        const stepNum = parseInt(ind.dataset.step);
        ind.classList.toggle('active', stepNum === currentStep);
        ind.classList.toggle('completed', stepNum < currentStep);
      });

      // Controls buttons toggle
      if (backBtn) {
        backBtn.style.visibility = (currentStep === 1) ? 'hidden' : 'visible';
      }

      if (currentStep === totalSteps) {
        if (nextBtn) nextBtn.style.display = 'none';
        if (submitBtn) submitBtn.style.display = 'inline-flex';
      } else {
        if (nextBtn) nextBtn.style.display = 'inline-flex';
        if (submitBtn) submitBtn.style.display = 'none';
      }

      if (currentStep === 4) {
        populateReviewSummary();
      }
    };

    if (nextBtn) {
      nextBtn.addEventListener('click', () => {
        if (validateStep(currentStep)) {
          if (currentStep < totalSteps) {
            currentStep++;
            transitionStep();
            window.scrollTo({ top: 0, behavior: 'smooth' });
          }
        }
      });
    }

    if (backBtn) {
      backBtn.addEventListener('click', () => {
        if (currentStep > 1) {
          currentStep--;
          transitionStep();
          window.scrollTo({ top: 0, behavior: 'smooth' });
        }
      });
    }

    // Load initial layout
    transitionStep();
  }

  // 5. BUTTON RIPPLE CLICK DECORATOR
  const btnElements = document.querySelectorAll('.btn');
  btnElements.forEach(btn => {
    btn.addEventListener('click', function(e) {
      const boundaries = this.getBoundingClientRect();
      const clickX = e.clientX - boundaries.left;
      const clickY = e.clientY - boundaries.top;

      const rippleCircle = document.createElement('span');
      rippleCircle.className = 'ripple';
      rippleCircle.style.left = `${clickX}px`;
      rippleCircle.style.top = `${clickY}px`;

      this.appendChild(rippleCircle);
      setTimeout(() => {
        rippleCircle.remove();
      }, 600);
    });
  });

});
