/* ============================================================
   CreditGuard AI — Premium Frontend Controller
   Client Interactions, Form Wizard, Theme Toggles & Page Loaders
   ============================================================ */

document.addEventListener('DOMContentLoaded', () => {
  
  // 1. PAGE LOADER INITIALIZATION
  const loader = document.getElementById('pageLoader');
  if (loader) {
    // Hide loader immediately after DOM rendering finishes
    setTimeout(() => {
      loader.classList.add('hidden');
    }, 200);
  }

  // 2. THEME CONTROLLER (Dark / Light Preference)
  const themeToggle = document.getElementById('themeToggle');
  const savedTheme = localStorage.getItem('theme') || 'dark';
  
  // Set initial preference
  document.documentElement.setAttribute('data-theme', savedTheme);
  if (themeToggle) {
    themeToggle.checked = (savedTheme === 'dark');
    
    themeToggle.addEventListener('change', () => {
      const activeTheme = themeToggle.checked ? 'dark' : 'light';
      document.documentElement.setAttribute('data-theme', activeTheme);
      localStorage.setItem('theme', activeTheme);
    });
  }

  // 3. RESPONSIVE MOBILE SIDEBAR TOGGLES
  const menuToggle = document.getElementById('menuToggle');
  const sidebar = document.getElementById('sidebar');
  const overlay = document.getElementById('sidebarOverlay');

  if (menuToggle && sidebar && overlay) {
    const toggleMenu = () => {
      sidebar.classList.toggle('open');
      overlay.classList.toggle('active');
    };

    menuToggle.addEventListener('click', toggleMenu);
    overlay.addEventListener('click', toggleMenu);
  }

  // 4. MULTI-STEP WIZARD ENGINE
  const wizardForm = document.getElementById('wizardForm');
  if (wizardForm) {
    const panels = Array.from(document.querySelectorAll('.wizard-panel'));
    const indicators = Array.from(document.querySelectorAll('.wizard-step-indicator'));
    const fill = document.getElementById('wizardProgressFill');
    
    const backBtn = document.getElementById('wizardBack');
    const nextBtn = document.getElementById('wizardNext');
    const submitBtn = document.getElementById('wizardSubmit');
    
    let currentStep = 1;

    // Validate fields inside current step
    const validateStep = (step) => {
      const activePanel = panels.find(p => p.dataset.step === String(step));
      if (!activePanel) return true;

      // Find required form elements in the panel
      const inputs = Array.from(activePanel.querySelectorAll('input, select, textarea'));
      let valid = true;

      inputs.forEach(input => {
        // Clear old errors
        const group = input.closest('.form-group');
        if (group) {
          const oldError = group.querySelector('.form-error');
          if (oldError) oldError.remove();
        }

        // Validate basic parameters
        if (input.hasAttribute('required') && !input.value.trim()) {
          valid = false;
          showInputError(input, 'This field is required.');
        } else if (input.id === 'age_years' && input.value) {
          const val = parseFloat(input.value);
          if (isNaN(val) || val < 18 || val > 100) {
            valid = false;
            showInputError(input, 'Age must be between 18 and 100.');
          }
        } else if (input.id === 'amt_income_total' && input.value) {
          const val = parseFloat(input.value);
          if (isNaN(val) || val <= 0) {
            valid = false;
            showInputError(input, 'Income must be a positive value.');
          }
        }
      });

      return valid;
    };

    const showInputError = (input, msg) => {
      const group = input.closest('.form-group');
      if (group) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'form-error animate-slide-down';
        errorDiv.textContent = msg;
        group.appendChild(errorDiv);
      }
    };

    // Update review summary panel (Step 3)
    const populateReviewSummary = () => {
      const reviewDiv = document.getElementById('reviewSummary');
      if (!reviewDiv) return;
      
      reviewDiv.innerHTML = '';
      
      const fieldMappings = [
        { label: 'Gender', id: 'code_gender' },
        { label: 'Age', id: 'age_years', suffix: ' Years' },
        { label: 'Marital Status', id: 'name_family_status' },
        { label: 'Children', id: 'cnt_children' },
        { label: 'Education', id: 'name_education_type' },
        { label: 'Housing Type', id: 'name_housing_type' },
        { label: 'Occupation', id: 'occupation_type' },
        { label: 'Income Source', id: 'name_income_type' },
        { label: 'Annual Income', id: 'amt_income_total', prefix: '$' },
        { label: 'Employment Years', id: 'years_employed', suffix: ' Yrs' },
        { label: 'Existing Monthly Debt', id: 'existing_debt', prefix: '$' },
        { label: 'Requested Limit', id: 'loan_amount', prefix: '$' },
        { label: 'Credit Rating', id: 'credit_history' }
      ];

      fieldMappings.forEach(item => {
        const el = document.getElementById(item.id);
        if (el) {
          let val = '';
          if (el.tagName === 'SELECT') {
            val = el.options[el.selectedIndex].text;
          } else {
            val = el.value || 'N/A';
          }
          
          if (item.prefix && val !== 'N/A') val = item.prefix + val;
          if (item.suffix && val !== 'N/A') val = val + item.suffix;

          const detailBlock = document.createElement('div');
          detailBlock.style.padding = '8px';
          detailBlock.innerHTML = `
            <span style="font-size:11px;color:var(--text-muted);display:block;text-transform:uppercase;">${item.label}</span>
            <span style="font-size:14px;font-weight:600;color:var(--text-primary);">${val}</span>
          `;
          reviewDiv.appendChild(detailBlock);
        }
      });
    };

    // Render step change layouts
    const updateWizard = () => {
      // Toggle panel visibility
      panels.forEach(p => {
        p.classList.toggle('active', p.dataset.step === String(currentStep));
      });

      // Update progress bar
      if (fill) {
        const percentage = ((currentStep - 1) / (panels.length - 1)) * 100;
        fill.style.width = `${percentage}%`;
      }

      // Update step indicator circles
      indicators.forEach(ind => {
        const stepNum = parseInt(ind.dataset.step);
        ind.classList.toggle('active', stepNum === currentStep);
        ind.classList.toggle('completed', stepNum < currentStep);
      });

      // Navigation button visibility checks
      if (backBtn) {
        backBtn.style.visibility = (currentStep === 1) ? 'hidden' : 'visible';
      }

      if (currentStep === panels.length) {
        if (nextBtn) nextBtn.style.display = 'none';
        if (submitBtn) submitBtn.style.display = 'inline-flex';
      } else {
        if (nextBtn) nextBtn.style.display = 'inline-flex';
        if (submitBtn) submitBtn.style.display = 'none';
      }

      // Populate review step when entering Step 3
      if (currentStep === 3) {
        populateReviewSummary();
      }
    };

    // Navigation trigger handlers
    if (nextBtn) {
      nextBtn.addEventListener('click', () => {
        if (validateStep(currentStep)) {
          if (currentStep < panels.length) {
            currentStep++;
            updateWizard();
            window.scrollTo({ top: 0, behavior: 'smooth' });
          }
        }
      });
    }

    if (backBtn) {
      backBtn.addEventListener('click', () => {
        if (currentStep > 1) {
          currentStep--;
          updateWizard();
          window.scrollTo({ top: 0, behavior: 'smooth' });
        }
      });
    }

    // Initialize layout
    updateWizard();
  }

  // 5. BUTTON RIPPLE CLICK ANIMATION
  const rippleButtons = document.querySelectorAll('.btn');
  rippleButtons.forEach(btn => {
    btn.addEventListener('click', function(e) {
      const rect = this.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;
      
      const ripple = document.createElement('span');
      ripple.className = 'ripple';
      ripple.style.left = `${x}px`;
      ripple.style.top = `${y}px`;
      
      this.appendChild(ripple);
      setTimeout(() => ripple.remove(), 600);
    });
  });

});
