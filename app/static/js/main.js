/* ═══════════════════════════════════════════════════════════════════════════
   CreditGuard AI — Application Controller v3.0
   ═══════════════════════════════════════════════════════════════════════════ */
'use strict';

const CG = (() => {

  /* ── Theme Manager ── */
  const Theme = {
    KEY: 'cg-theme',
    get() { return localStorage.getItem(this.KEY) || 'dark'; },
    set(t) { localStorage.setItem(this.KEY, t); document.documentElement.setAttribute('data-theme', t); },
    toggle() { this.set(this.get() === 'dark' ? 'light' : 'dark'); this.updateIcon(); },
    updateIcon() {
      const btn = document.getElementById('themeToggle');
      if (!btn) return;
      const icon = btn.querySelector('i');
      if (icon) { icon.className = this.get() === 'dark' ? 'fa-solid fa-sun' : 'fa-solid fa-moon'; }
    },
    init() { this.set(this.get()); this.updateIcon(); }
  };

  /* ── Page Loader ── */
  const Loader = {
    hide() {
      const el = document.getElementById('pageLoader');
      if (el) { el.classList.add('hidden'); setTimeout(() => el.remove(), 500); }
    }
  };

  /* ── Sidebar ── */
  const Sidebar = {
    toggle() {
      const sb = document.querySelector('.cg-sidebar');
      const ov = document.querySelector('.cg-overlay');
      sb?.classList.toggle('open');
      ov?.classList.toggle('active');
    },
    close() {
      document.querySelector('.cg-sidebar')?.classList.remove('open');
      document.querySelector('.cg-overlay')?.classList.remove('active');
    },
    init() {
      document.getElementById('menuBtn')?.addEventListener('click', this.toggle);
      document.querySelector('.cg-overlay')?.addEventListener('click', () => this.close());
    }
  };

  /* ── Counter Animation ── */
  const Counter = {
    animate(el) {
      const target = parseFloat(el.dataset.count);
      const suffix = el.dataset.suffix || '';
      const prefix = el.dataset.prefix || '';
      const decimals = (el.dataset.decimals || '0') | 0;
      const duration = 1800;
      const start = performance.now();
      const step = (now) => {
        const progress = Math.min((now - start) / duration, 1);
        const eased = 1 - Math.pow(1 - progress, 4);
        const current = target * eased;
        el.textContent = prefix + current.toFixed(decimals) + suffix;
        if (progress < 1) requestAnimationFrame(step);
      };
      requestAnimationFrame(step);
    },
    init() {
      const observer = new IntersectionObserver((entries) => {
        entries.forEach(e => { if (e.isIntersecting) { this.animate(e.target); observer.unobserve(e.target); } });
      }, { threshold: 0.3 });
      document.querySelectorAll('[data-count]').forEach(el => observer.observe(el));
    }
  };

  /* ── Scroll Reveal ── */
  const Reveal = {
    init() {
      const observer = new IntersectionObserver((entries) => {
        entries.forEach(e => {
          if (e.isIntersecting) {
            e.target.classList.add('cg-visible');
            observer.unobserve(e.target);
          }
        });
      }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });
      document.querySelectorAll('[data-reveal]').forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        el.style.transition = `opacity 0.6s var(--ease) ${el.dataset.reveal || '0s'}, transform 0.6s var(--ease) ${el.dataset.reveal || '0s'}`;
        observer.observe(el);
      });
    }
  };
  document.head.insertAdjacentHTML('beforeend', '<style>.cg-visible{opacity:1!important;transform:translateY(0)!important;}</style>');

  /* ── Wizard (Multi-step Form) ── */
  const Wizard = {
    current: 0,
    panels: [],
    nodes: [],
    lines: [],

    init() {
      this.panels = Array.from(document.querySelectorAll('.cg-wizard-panel'));
      this.nodes = Array.from(document.querySelectorAll('.cg-step-node'));
      this.lines = Array.from(document.querySelectorAll('.cg-step-line'));
      if (!this.panels.length) return;

      this.nodes.forEach((n, i) => n.addEventListener('click', () => { if (i <= this.current) this.goTo(i); }));
      document.querySelectorAll('[data-wizard-next]').forEach(b => b.addEventListener('click', () => this.next()));
      document.querySelectorAll('[data-wizard-prev]').forEach(b => b.addEventListener('click', () => this.prev()));
      this.goTo(0);
    },

    goTo(step) {
      this.current = step;
      this.panels.forEach((p, i) => p.classList.toggle('active', i === step));
      this.nodes.forEach((n, i) => { n.classList.remove('active', 'done'); if (i < step) n.classList.add('done'); else if (i === step) n.classList.add('active'); });
      this.lines.forEach((l, i) => l.classList.toggle('done', i < step));
    },
    next() { if (this.validate() && this.current < this.panels.length - 1) this.goTo(this.current + 1); },
    prev() { if (this.current > 0) this.goTo(this.current - 1); },

    validate() {
      const panel = this.panels[this.current];
      let valid = true;
      panel.querySelectorAll('[required]').forEach(field => {
        if (!field.value || field.value === '') {
          field.style.borderColor = 'var(--danger)';
          valid = false;
          field.addEventListener('input', () => { field.style.borderColor = ''; }, { once: true });
        }
      });
      if (!valid) Toast.show('Please fill in all required fields.', 'danger');
      return valid;
    }
  };

  /* ── Toast Notifications ── */
  const Toast = {
    init() {
      if (!document.querySelector('.cg-toast-stack')) {
        document.body.insertAdjacentHTML('beforeend', '<div class="cg-toast-stack" id="toastStack"></div>');
      }
    },
    show(msg, type = 'info', duration = 4000) {
      const stack = document.getElementById('toastStack');
      if (!stack) return;
      const icons = { success: 'fa-check-circle', danger: 'fa-exclamation-circle', info: 'fa-info-circle', warning: 'fa-exclamation-triangle' };
      const toast = document.createElement('div');
      toast.className = `cg-toast ${type}`;
      toast.innerHTML = `<i class="fa-solid ${icons[type] || icons.info} cg-toast-icon"></i><div><div style="font-size:13px;font-weight:600;color:var(--text-primary)">${msg}</div></div>`;
      stack.appendChild(toast);
      setTimeout(() => { toast.style.opacity = '0'; toast.style.transform = 'translateX(40px)'; setTimeout(() => toast.remove(), 300); }, duration);
    }
  };

  /* ── Gauge (Result Page) ── */
  const Gauge = {
    init() {
      const fill = document.querySelector('.cg-gauge-fill');
      if (!fill) return;
      const pct = parseFloat(fill.dataset.pct || 0);
      const circumference = 2 * Math.PI * 85;
      fill.style.strokeDasharray = circumference;
      fill.style.strokeDashoffset = circumference;
      requestAnimationFrame(() => {
        setTimeout(() => { fill.style.strokeDashoffset = circumference - (circumference * pct / 100); }, 300);
      });
    }
  };

  /* ── Chart.js Helpers ── */
  const Charts = {
    baseOpts: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: 'rgba(24,24,27,0.95)',
          borderColor: 'rgba(255,255,255,0.06)',
          borderWidth: 1,
          titleFont: { family: "'Inter'", size: 12, weight: 600 },
          bodyFont: { family: "'Inter'", size: 12 },
          padding: 12, cornerRadius: 8,
        }
      },
      scales: {
        x: { grid: { color: 'rgba(255,255,255,0.04)' }, ticks: { font: { family: "'Inter'", size: 11 }, color: '#71717a' } },
        y: { grid: { color: 'rgba(255,255,255,0.04)' }, ticks: { font: { family: "'Inter'", size: 11 }, color: '#71717a' } }
      }
    },
    doughnutOpts: {
      responsive: true,
      maintainAspectRatio: false,
      cutout: '72%',
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: 'rgba(24,24,27,0.95)',
          borderColor: 'rgba(255,255,255,0.06)',
          borderWidth: 1,
          padding: 12, cornerRadius: 8,
          titleFont: { family: "'Inter'", size: 12, weight: 600 },
          bodyFont: { family: "'Inter'", size: 12 },
        }
      }
    }
  };

  /* ── Ripple Click Effects ── */
  const Ripple = {
    create(e) {
      const btn = e.currentTarget;
      const rect = btn.getBoundingClientRect();
      const size = Math.max(rect.width, rect.height);
      const x = e.clientX - rect.left - size/2;
      const y = e.clientY - rect.top - size/2;
      
      const circle = document.createElement('span');
      circle.style.width = circle.style.height = `${size}px`;
      circle.style.left = `${x}px`;
      circle.style.top = `${y}px`;
      circle.classList.add('cg-ripple-span');
      
      const prevRipple = btn.querySelector('.cg-ripple-span');
      if (prevRipple) prevRipple.remove();
      
      btn.appendChild(circle);
      setTimeout(() => circle.remove(), 600);
    },
    init() {
      document.querySelectorAll('.cg-btn, .cg-tile-select, .cg-drawer-chip').forEach(btn => {
        btn.style.position = 'relative';
        btn.style.overflow = 'hidden';
        btn.addEventListener('mousedown', this.create);
      });
    }
  };

  /* ── Flash Message Handler ── */
  const Flash = {
    init() {
      document.querySelectorAll('[data-flash]').forEach(el => {
        const type = el.dataset.flash || 'info';
        Toast.show(el.textContent, type);
        el.remove();
      });
    }
  };

  /* ── Master Init ── */
  const init = () => {
    Theme.init();
    Sidebar.init();
    Toast.init();
    Flash.init();
    Counter.init();
    Reveal.init();
    Wizard.init();
    Gauge.init();
    Ripple.init();

    // Bind theme toggle
    document.getElementById('themeToggle')?.addEventListener('click', () => Theme.toggle());

    // Remove loader
    setTimeout(() => Loader.hide(), 400);
  };

  // Run
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();

  // Public API
  return { Theme, Toast, Wizard, Charts, Gauge };
})();
