/**
 * Rapid Cash - Alpine.js Data Components
 * Sidebar, Toast Notifications, Form Validation
 */

// Initialize Alpine data when Alpine is ready
document.addEventListener('alpine:init', () => {
  
  // ==========================================
  // SIDEBAR COMPONENT (Mobile Drawer)
  // ==========================================
  Alpine.data('sidebar', () => ({
    open: false,
    
    init() {
      // Close on escape key
      document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && this.open) {
          this.close();
        }
      });
      
      // Close on route change (mobile)
      document.addEventListener('click', (e) => {
        if (e.target.tagName === 'A' && this.open) {
          this.close();
        }
      });
    },
    
    toggle() {
      this.open = !this.open;
      this.toggleBodyScroll();
    },
    
    open() {
      this.open = true;
      this.toggleBodyScroll();
    },
    
    close() {
      this.open = false;
      this.toggleBodyScroll();
    },
    
    toggleBodyScroll() {
      document.body.classList.toggle('overflow-hidden', this.open);
    }
  }));
  
  // ==========================================
  // TOAST NOTIFICATION SYSTEM
  // ==========================================
  Alpine.data('toastSystem', () => ({
    toasts: [],
    maxToasts: 5,
    
    add(message, type = 'info', duration = 4000) {
      const id = Date.now() + Math.random();
      
      // Remove oldest toast if max reached
      if (this.toasts.length >= this.maxToasts) {
        this.toasts.shift();
      }
      
      this.toasts.push({ 
        id, 
        message, 
        type,
        icon: this.getIcon(type)
      });
      
      // Auto remove after duration
      setTimeout(() => {
        this.remove(id);
      }, duration);
    },
    
    remove(id) {
      const index = this.toasts.findIndex(t => t.id === id);
      if (index > -1) {
        this.toasts.splice(index, 1);
      }
    },
    
    getIcon(type) {
      const icons = {
        success: `<svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/></svg>`,
        error: `<svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>`,
        warning: `<svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/></svg>`,
        info: `<svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>`
      };
      return icons[type] || icons.info;
    },
    
    // Convenience methods
    success(message) { this.add(message, 'success'); },
    error(message) { this.add(message, 'error'); },
    warning(message) { this.add(message, 'warning'); },
    info(message) { this.add(message, 'info'); }
  }));
  
  // ==========================================
  // FORM VALIDATION
  // ==========================================
  Alpine.data('formValidation', (fields = {}) => ({
    errors: {},
    touched: {},
    values: fields,
    loading: false,
    
    touch(field) {
      this.touched[field] = true;
    },
    
    validate(field, rules = []) {
      this.touch(field);
      const value = this.values[field];
      
      for (const rule of rules) {
        const error = this.checkRule(value, rule, field);
        if (error) {
          this.errors[field] = error;
          return false;
        }
      }
      
      delete this.errors[field];
      return true;
    },
    
    checkRule(value, rule, field) {
      if (rule === 'required' && (!value || value.toString().trim() === '')) {
        return 'Ce champ est requis';
      }
      
      if (rule === 'number' && value && isNaN(parseFloat(value))) {
        return 'Veuillez entrer un nombre valide';
      }
      
      if (rule === 'email' && value && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) {
        return 'Adresse email invalide';
      }
      
      if (rule.startsWith('min:')) {
        const min = parseFloat(rule.split(':')[1]);
        if (parseFloat(value) < min) {
          return `Minimum ${min}`;
        }
      }
      
      if (rule.startsWith('max:')) {
        const max = parseFloat(rule.split(':')[1]);
        if (parseFloat(value) > max) {
          return `Maximum ${max}`;
        }
      }
      
      return null;
    },
    
    isValid(field) {
      return this.touched[field] && !this.errors[field];
    },
    
    hasError(field) {
      return this.touched[field] && this.errors[field];
    },
    
    get isFormValid() {
      return Object.keys(this.errors).length === 0 && 
             Object.keys(this.touched).length === Object.keys(this.values).length;
    },
    
    async submit(callback) {
      // Validate all fields
      for (const [field, value] of Object.entries(this.values)) {
        this.validate(field, value.rules || ['required']);
      }
      
      if (Object.keys(this.errors).length > 0) {
        return false;
      }
      
      this.loading = true;
      try {
        await callback();
        return true;
      } catch (error) {
        console.error('Form submission error:', error);
        return false;
      } finally {
        this.loading = false;
      }
    }
  }));
  
  // ==========================================
  // OPERATION FORM (Optimized for speed)
  // ==========================================
  Alpine.data('operationForm', () => ({
    step: 1,
    type: '',
    amount: '',
    currency: 'USD',
    loading: false,
    currencies: ['USD', 'CDF', 'EUR', 'TL'],
    
    get calculatedFee() {
      if (!this.amount) return '0.00';
      return (parseFloat(this.amount) * 0.02).toFixed(2);
    },
    
    get totalAmount() {
      if (!this.amount) return '0.00';
      return (parseFloat(this.amount) + parseFloat(this.calculatedFee)).toFixed(2);
    },
    
    get convertedAmount() {
      // Mock conversion rates
      const rates = { USD: 1, CDF: 0.000357, EUR: 1.09, TL: 0.031 };
      if (!this.amount) return '0.00';
      return (parseFloat(this.amount) * rates[this.currency]).toFixed(2);
    },
    
    selectType(type) {
      this.type = type;
    },
    
    selectCurrency(curr) {
      this.currency = curr;
    },
    
    nextStep() {
      if (this.step === 1 && this.type && this.amount) {
        this.step = 2;
      }
    },
    
    prevStep() {
      if (this.step > 1) {
        this.step--;
      }
    },
    
    async submit() {
      this.loading = true;
      
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      // Dispatch toast event
      window.dispatchEvent(new CustomEvent('toast', {
        detail: { type: 'success', message: 'Opération enregistrée avec succès!' }
      }));
      
      this.loading = false;
      
      // Redirect to dashboard
      window.location.href = '/dashboard/';
    },
    
    reset() {
      this.step = 1;
      this.type = '';
      this.amount = '';
      this.currency = 'USD';
      this.loading = false;
    }
  }));
  
  // ==========================================
  // LOADING STATES
  // ==========================================
  Alpine.data('loadingButton', () => ({
    loading: false,
    
    start() { this.loading = true; },
    stop() { this.loading = false; }
  }));
  
  // ==========================================
  // DROPDOWN MENU
  // ==========================================
  Alpine.data('dropdown', () => ({
    open: false,
    
    toggle() {
      this.open = !this.open;
    },
    
    close() {
      this.open = false;
    },
    
    init() {
      // Close when clicking outside
      document.addEventListener('click', (e) => {
        if (!this.$el.contains(e.target)) {
          this.close();
        }
      });
    }
  }));
  
  // ==========================================
  // COLLAPSE / ACCORDION
  // ==========================================
  Alpine.data('collapse', () => ({
    open: false,
    
    toggle() {
      this.open = !this.open;
    }
  }));
  
});

// ==========================================
// GLOBAL TOAST HELPER
// ==========================================
window.toast = function(message, type = 'info', duration = 4000) {
  window.dispatchEvent(new CustomEvent('toast', {
    detail: { message, type, duration }
  }));
};

// Toast shortcuts
window.toast.success = (msg) => window.toast(msg, 'success');
window.toast.error = (msg) => window.toast(msg, 'error');
window.toast.warning = (msg) => window.toast(msg, 'warning');
window.toast.info = (msg) => window.toast(msg, 'info');
