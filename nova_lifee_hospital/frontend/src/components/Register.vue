<template>
  <div class="register-page">
    <div class="register-ambient-glow"></div>

    <div class="register-card-container">
      <!-- Card Header -->
      <div class="register-card-header">
        <div class="header-icon-circle">
          <i class="bi bi-person-plus-fill"></i>
        </div>
        <div class="header-text-block">
          <div class="header-tag">NEW PATIENT ENROLLMENT</div>
          <h2 class="register-title">Create Your Patient Account</h2>
          <p class="register-subtitle">Register to consult top specialists, manage digital prescriptions, and track clinical appointments.</p>
        </div>
      </div>

      <!-- Registration Form -->
      <form @submit.prevent="register" class="register-form">
        <!-- Two Column Form Grid -->
        <div class="form-grid-2col">
          <!-- Column 1: Account Credentials -->
          <div class="form-col">
            <h5 class="col-section-title"><i class="bi bi-person-lock me-1"></i> Account Credentials</h5>
            
            <!-- Full Name -->
            <div class="form-field-group">
              <label class="form-label" for="reg-name">Full Name <span class="required-star">*</span></label>
              <div class="input-control-wrapper">
                <i class="bi bi-person input-prefix-icon"></i>
                <input
                  id="reg-name"
                  v-model="form.name"
                  type="text"
                  required
                  class="saas-input"
                  placeholder="e.g. John Doe"
                />
              </div>
            </div>

            <!-- Email -->
            <div class="form-field-group">
              <label class="form-label" for="reg-email">Email Address <span class="required-star">*</span></label>
              <div class="input-control-wrapper">
                <i class="bi bi-envelope input-prefix-icon"></i>
                <input
                  id="reg-email"
                  v-model="form.email"
                  type="email"
                  required
                  class="saas-input"
                  placeholder="name@example.com"
                />
              </div>
            </div>

            <!-- Password -->
            <div class="form-field-group">
              <label class="form-label" for="reg-password">Password <span class="required-star">*</span></label>
              <div class="input-control-wrapper">
                <i class="bi bi-lock input-prefix-icon"></i>
                <input
                  id="reg-password"
                  v-model="form.password"
                  :type="showPassword ? 'text' : 'password'"
                  required
                  minlength="6"
                  class="saas-input"
                  placeholder="Minimum 6 characters"
                />
                <button
                  type="button"
                  class="btn-toggle-password"
                  @click="showPassword = !showPassword"
                  aria-label="Toggle password visibility"
                >
                  <i :class="showPassword ? 'bi bi-eye-slash' : 'bi bi-eye'"></i>
                </button>
              </div>
            </div>
          </div>

          <!-- Column 2: Patient Contact & Medical Info -->
          <div class="form-col">
            <h5 class="col-section-title"><i class="bi bi-geo-alt me-1"></i> Contact & Demographics</h5>
            
            <!-- Phone Number -->
            <div class="form-field-group">
              <label class="form-label" for="reg-phone">Phone Number</label>
              <div class="input-control-wrapper">
                <i class="bi bi-telephone input-prefix-icon"></i>
                <input
                  id="reg-phone"
                  v-model="form.phone"
                  type="tel"
                  class="saas-input"
                  placeholder="e.g. +1 (555) 019-2834"
                />
              </div>
            </div>

            <!-- Gender -->
            <div class="form-field-group">
              <label class="form-label" for="reg-gender">Gender</label>
              <div class="input-control-wrapper">
                <i class="bi bi-gender-ambiguous input-prefix-icon"></i>
                <select id="reg-gender" v-model="form.gender" class="saas-select">
                  <option value="" disabled selected>Select Gender</option>
                  <option value="Male">Male</option>
                  <option value="Female">Female</option>
                  <option value="Others">Others</option>
                </select>
                <i class="bi bi-chevron-down select-chevron-icon"></i>
              </div>
            </div>

            <!-- Address -->
            <div class="form-field-group">
              <label class="form-label" for="reg-address">Residential Address</label>
              <div class="input-control-wrapper">
                <textarea
                  id="reg-address"
                  v-model="form.address"
                  rows="2"
                  class="saas-textarea"
                  placeholder="Street address, city, state, postal code"
                ></textarea>
              </div>
            </div>
          </div>
        </div>

        <!-- Feedback Alerts -->
        <div v-if="msg" class="saas-alert saas-alert-success">
          <i class="bi bi-check-circle-fill alert-icon"></i>
          <div class="alert-content">
            <strong>Success!</strong> {{ msg }}
            <div class="mt-2">
              <router-link to="/login" class="btn-goto-login">
                Proceed to Login <i class="bi bi-arrow-right ms-1"></i>
              </router-link>
            </div>
          </div>
          <button type="button" class="alert-dismiss" @click="msg = ''">✕</button>
        </div>

        <div v-if="error" class="saas-alert saas-alert-danger">
          <i class="bi bi-exclamation-triangle-fill alert-icon"></i>
          <div class="alert-content">
            <span>{{ error }}</span>
          </div>
          <button type="button" class="alert-dismiss" @click="error = ''">✕</button>
        </div>

        <!-- Submit & Navigation -->
        <div class="form-actions-row">
          <button type="submit" class="btn-register-submit" :disabled="loading">
            <span v-if="loading" class="spinner-border spinner-border-sm me-2" role="status"></span>
            <span v-if="!loading">Complete Patient Registration</span>
            <span v-else>Registering Patient...</span>
            <i v-if="!loading" class="bi bi-arrow-right ms-2"></i>
          </button>
        </div>
      </form>

      <div class="register-card-footer">
        <p>Already have an active patient account? <router-link to="/login" class="auth-link">Sign In Here</router-link></p>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'Register',
  data() {
    return {
      form: {
        name: '',
        email: '',
        password: '',
        phone: '',
        gender: '',
        address: ''
      },
      msg: '',
      error: '',
      loading: false,
      showPassword: false
    }
  },
  methods: {
    async register() {
      this.error = ''
      this.msg = ''
      this.loading = true

      try {
        const res = await axios.post('https://nova-life-hospital.onrender.com/api/register', this.form)
        this.msg = res.data.message || 'Patient registered successfully! You can now sign in.'
        this.error = ''
        // Reset form upon successful registration
        this.form = { name: '', email: '', password: '', phone: '', gender: '', address: '' }
      } catch (e) {
        this.error = e.response?.data?.error || 'Server error occurred during registration. Please try again.'
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
.register-page {
  position: relative;
  min-height: calc(100vh - 72px);
  background: linear-gradient(135deg, var(--slate-950) 0%, var(--slate-900) 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 48px 24px;
  overflow: hidden;
}

.register-ambient-glow {
  position: absolute;
  width: 800px;
  height: 800px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(16, 185, 129, 0.12) 0%, rgba(2, 132, 199, 0.08) 50%, rgba(0, 0, 0, 0) 70%);
  filter: blur(140px);
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  pointer-events: none;
}

.register-card-container {
  position: relative;
  z-index: 1;
  width: 100%;
  max-width: 920px;
  background: rgba(15, 23, 42, 0.85);
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: var(--radius-xl);
  padding: 44px 48px;
  backdrop-filter: blur(20px);
  box-shadow: 0 25px 60px -12px rgba(0, 0, 0, 0.6);
}

/* ==========================================================================
   HEADER
   ========================================================================== */
.register-card-header {
  display: flex;
  align-items: flex-start;
  gap: 20px;
  margin-bottom: 36px;
  padding-bottom: 24px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
}

.header-icon-circle {
  width: 52px;
  height: 52px;
  border-radius: var(--radius-lg);
  background: linear-gradient(135deg, #059669, #10b981);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  box-shadow: 0 4px 14px rgba(16, 185, 129, 0.35);
  flex-shrink: 0;
}

.header-tag {
  font-size: 11.5px;
  font-weight: 700;
  color: #34d399;
  letter-spacing: 1.2px;
  margin-bottom: 4px;
}

.register-title {
  font-size: 26px;
  font-weight: 800;
  color: white;
  margin-bottom: 4px;
}

.register-subtitle {
  font-size: 14px;
  color: var(--slate-400);
  line-height: 1.5;
  margin-bottom: 0;
}

/* ==========================================================================
   FORM GRID
   ========================================================================== */
.form-grid-2col {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 36px;
  margin-bottom: 24px;
}

.col-section-title {
  font-size: 14px;
  font-weight: 700;
  color: #38bdf8;
  margin-bottom: 18px;
  letter-spacing: 0.2px;
}

.form-field-group {
  margin-bottom: 18px;
}

.form-label {
  display: block;
  font-size: 13px;
  font-weight: 600;
  color: var(--slate-300);
  margin-bottom: 6px;
}

.required-star {
  color: #f87171;
}

.input-control-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.input-prefix-icon {
  position: absolute;
  left: 14px;
  font-size: 15px;
  color: var(--slate-400);
  pointer-events: none;
}

.saas-input,
.saas-select,
.saas-textarea {
  width: 100%;
  background: rgba(15, 23, 42, 0.6);
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: var(--radius-md);
  font-size: 14px;
  font-family: var(--font-primary);
  color: white;
  outline: none;
  transition: var(--transition-smooth);
}

.saas-input {
  padding: 11px 14px 11px 40px;
}

.saas-select {
  padding: 11px 36px 11px 40px;
  appearance: none;
  -webkit-appearance: none;
  cursor: pointer;
}

.saas-select option {
  background: var(--slate-900);
  color: white;
}

.select-chevron-icon {
  position: absolute;
  right: 14px;
  font-size: 12px;
  color: var(--slate-400);
  pointer-events: none;
}

.saas-textarea {
  padding: 10px 14px;
  resize: vertical;
  min-height: 80px;
}

.saas-input:focus,
.saas-select:focus,
.saas-textarea:focus {
  border-color: #10b981;
  background: rgba(15, 23, 42, 0.9);
  box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.2);
}

.saas-input::placeholder,
.saas-textarea::placeholder {
  color: var(--slate-500);
}

.btn-toggle-password {
  position: absolute;
  right: 12px;
  background: transparent;
  border: none;
  color: var(--slate-400);
  cursor: pointer;
  padding: 4px;
  font-size: 15px;
}

.btn-toggle-password:hover {
  color: white;
}

/* Alerts */
.saas-alert {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 14px 18px;
  border-radius: var(--radius-md);
  margin-bottom: 24px;
  font-size: 13.5px;
}

.saas-alert-success {
  background: rgba(16, 185, 129, 0.15);
  border: 1px solid rgba(16, 185, 129, 0.35);
  color: #6ee7b7;
}

.saas-alert-danger {
  background: rgba(239, 68, 68, 0.15);
  border: 1px solid rgba(239, 68, 68, 0.35);
  color: #fca5a5;
}

.alert-icon {
  font-size: 18px;
  margin-top: 1px;
}

.saas-alert-success .alert-icon { color: #10b981; }
.saas-alert-danger .alert-icon { color: #ef4444; }

.alert-content {
  flex: 1;
}

.alert-dismiss {
  background: transparent;
  border: none;
  color: inherit;
  cursor: pointer;
  font-size: 14px;
  padding: 0;
  opacity: 0.8;
}

.btn-goto-login {
  display: inline-flex;
  align-items: center;
  padding: 6px 14px;
  background: #10b981;
  color: white;
  font-weight: 700;
  font-size: 12.5px;
  border-radius: var(--radius-sm);
  text-decoration: none;
  transition: var(--transition-smooth);
}

.btn-goto-login:hover {
  background: #059669;
  color: white;
}

/* Submit */
.btn-register-submit {
  width: 100%;
  padding: 14px;
  background: linear-gradient(135deg, #059669 0%, #10b981 100%);
  color: white;
  border: none;
  border-radius: var(--radius-md);
  font-size: 15.5px;
  font-weight: 700;
  font-family: var(--font-primary);
  cursor: pointer;
  transition: var(--transition-smooth);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 14px rgba(16, 185, 129, 0.35);
}

.btn-register-submit:hover:not(:disabled) {
  background: linear-gradient(135deg, #047857 0%, #059669 100%);
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(16, 185, 129, 0.45);
}

.btn-register-submit:disabled {
  opacity: 0.65;
  cursor: not-allowed;
}

/* Footer */
.register-card-footer {
  margin-top: 28px;
  padding-top: 20px;
  border-top: 1px solid rgba(255, 255, 255, 0.08);
  text-align: center;
}

.register-card-footer p {
  font-size: 13.5px;
  color: var(--slate-400);
  margin-bottom: 0;
}

.auth-link {
  color: #34d399;
  text-decoration: none;
  font-weight: 600;
  margin-left: 4px;
  transition: var(--transition-smooth);
}

.auth-link:hover {
  color: white;
  text-decoration: underline;
}

/* ==========================================================================
   RESPONSIVENESS
   ========================================================================== */
@media (max-width: 768px) {
  .register-card-container {
    padding: 32px 24px;
  }

  .form-grid-2col {
    grid-template-columns: 1fr;
    gap: 20px;
  }

  .register-card-header {
    flex-direction: column;
    gap: 14px;
  }
}
</style>