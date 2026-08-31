<template>
  <div class="auth-page">
    <div class="auth-ambient-glow"></div>

    <div class="auth-layout-container">
      <!-- Left Healthcare Brand Showcase Column -->
      <div class="auth-showcase-panel">
        <div class="showcase-content">
          <div class="showcase-badge">
            <i class="bi bi-shield-check me-1"></i> SECURE HEALTHCARE ACCESS
          </div>
          <h2 class="showcase-title">Enterprise Clinical Management Platform</h2>
          <p class="showcase-desc">
            Unified access for hospital administrators, certified medical doctors, and registered patients with enterprise security.
          </p>

          <div class="showcase-features">
            <div class="showcase-feat-item">
              <div class="feat-bullet"><i class="bi bi-check-lg"></i></div>
              <div>
                <strong>Role-Based Security</strong>
                <span>Dedicated administrative and clinical consoles</span>
              </div>
            </div>

            <div class="showcase-feat-item">
              <div class="feat-bullet"><i class="bi bi-check-lg"></i></div>
              <div>
                <strong>Electronic Health Records</strong>
                <span>Real-time prescription and diagnosis tracking</span>
              </div>
            </div>

            <div class="showcase-feat-item">
              <div class="feat-bullet"><i class="bi bi-check-lg"></i></div>
              <div>
                <strong>7-Day Specialist Schedules</strong>
                <span>Automated doctor availability and slot management</span>
              </div>
            </div>
          </div>
        </div>

        <div class="showcase-footer">
          <div class="compliance-tag">
            <i class="bi bi-lock-fill me-1"></i> TLS 1.3 256-Bit SSL Encrypted Connection
          </div>
        </div>
      </div>

      <!-- Right Login Card Form -->
      <div class="auth-form-panel">
        <div class="auth-card">
          <div class="auth-card-header">
            <div class="auth-icon-circle">
              <i class="bi bi-person-badge"></i>
            </div>
            <h3 class="auth-title">Welcome Back</h3>
            <p class="auth-subtitle">Sign in to access your NovaLife portal</p>
          </div>

          <form @submit.prevent="login" class="auth-form">
            <!-- Email Input -->
            <div class="form-field-group">
              <label class="form-label" for="login-email">Email Address</label>
              <div class="input-control-wrapper">
                <i class="bi bi-envelope input-prefix-icon"></i>
                <input
                  id="login-email"
                  v-model="email"
                  type="email"
                  required
                  class="saas-input"
                  placeholder="name@hospital.com"
                  autocomplete="email"
                />
              </div>
            </div>

            <!-- Password Input -->
            <div class="form-field-group">
              <div class="label-row">
                <label class="form-label" for="login-password">Password</label>
              </div>
              <div class="input-control-wrapper">
                <i class="bi bi-lock input-prefix-icon"></i>
                <input
                  id="login-password"
                  v-model="password"
                  :type="showPassword ? 'text' : 'password'"
                  required
                  class="saas-input"
                  placeholder="••••••••••••"
                  autocomplete="current-password"
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

            <!-- Error Banner -->
            <div v-if="error" class="saas-alert saas-alert-danger">
              <i class="bi bi-exclamation-triangle-fill alert-icon"></i>
              <div class="alert-content">
                <span>{{ error }}</span>
              </div>
              <button type="button" class="alert-dismiss" @click="error = ''">✕</button>
            </div>

            <!-- Submit Button -->
            <button type="submit" class="btn-auth-submit" :disabled="loading">
              <span v-if="loading" class="spinner-border spinner-border-sm me-2" role="status"></span>
              <span v-if="!loading">Authenticate & Enter Portal</span>
              <span v-else>Signing in...</span>
              <i v-if="!loading" class="bi bi-arrow-right ms-2"></i>
            </button>
          </form>

          <div class="auth-card-footer">
            <p>
              New patient requiring treatment?
              <router-link to="/register" class="auth-link">Register an Account</router-link>
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'Login',
  data() {
    return {
      email: '',
      password: '',
      error: '',
      loading: false,
      showPassword: false
    }
  },
  methods: {
    async login() {
      this.error = ''
      this.loading = true

      try {
        const res = await axios.post('https://nova-life-hospital.onrender.com/api/login', {
          email: this.email,
          password: this.password
        })

        localStorage.setItem('name', res.data.name)
        localStorage.setItem('user_id', res.data.user_id)
        localStorage.setItem('role', res.data.role)

        // Dispatch storage event for instant navbar sync
        window.dispatchEvent(new Event('storage'))

        if (res.data.role === 'admin') {
          this.$router.push('/admin')
        } else if (res.data.role === 'doctor') {
          this.$router.push('/doctor')
        } else {
          this.$router.push('/patient')
        }
      } catch (err) {
        this.error = err.response?.data?.error || 'Invalid login credentials. Please verify your email and password.'
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
.auth-page {
  position: relative;
  min-height: calc(100vh - 72px);
  background: linear-gradient(135deg, var(--slate-950) 0%, var(--slate-900) 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px 24px;
  overflow: hidden;
}

.auth-ambient-glow {
  position: absolute;
  width: 700px;
  height: 700px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(14, 165, 233, 0.15) 0%, rgba(99, 102, 241, 0) 70%);
  filter: blur(120px);
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  pointer-events: none;
}

.auth-layout-container {
  position: relative;
  z-index: 1;
  width: 100%;
  max-width: 1060px;
  display: grid;
  grid-template-columns: 1fr 1fr;
  background: rgba(15, 23, 42, 0.75);
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: var(--radius-xl);
  backdrop-filter: blur(20px);
  box-shadow: 0 25px 60px -12px rgba(0, 0, 0, 0.6);
  overflow: hidden;
}

/* ==========================================================================
   LEFT SHOWCASE PANEL
   ========================================================================== */
.auth-showcase-panel {
  background: linear-gradient(135deg, rgba(2, 132, 199, 0.15) 0%, rgba(37, 99, 235, 0.25) 100%);
  border-right: 1px solid rgba(255, 255, 255, 0.1);
  padding: 48px 40px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  color: white;
}

.showcase-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: rgba(56, 189, 248, 0.15);
  border: 1px solid rgba(56, 189, 248, 0.3);
  padding: 6px 14px;
  border-radius: var(--radius-full);
  font-size: 11px;
  font-weight: 700;
  color: #38bdf8;
  letter-spacing: 1px;
  margin-bottom: 24px;
}

.showcase-title {
  font-size: 28px;
  font-weight: 800;
  line-height: 1.25;
  color: white;
  margin-bottom: 14px;
}

.showcase-desc {
  font-size: 14.5px;
  color: var(--slate-300);
  line-height: 1.6;
  margin-bottom: 32px;
}

.showcase-features {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.showcase-feat-item {
  display: flex;
  align-items: flex-start;
  gap: 12px;
}

.feat-bullet {
  width: 26px;
  height: 26px;
  border-radius: 50%;
  background: #0284c7;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  flex-shrink: 0;
}

.showcase-feat-item strong {
  display: block;
  font-size: 13.5px;
  color: white;
  font-weight: 600;
}

.showcase-feat-item span {
  font-size: 12.5px;
  color: var(--slate-400);
}

.compliance-tag {
  font-size: 11.5px;
  color: var(--slate-400);
  padding-top: 24px;
}

/* ==========================================================================
   RIGHT FORM PANEL
   ========================================================================== */
.auth-form-panel {
  padding: 48px 42px;
  background: rgba(255, 255, 255, 0.02);
}

.auth-card {
  width: 100%;
}

.auth-card-header {
  text-align: left;
  margin-bottom: 24px;
}

.auth-icon-circle {
  width: 48px;
  height: 48px;
  border-radius: var(--radius-md);
  background: linear-gradient(135deg, #0284c7, #2563eb);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 22px;
  margin-bottom: 16px;
  box-shadow: 0 4px 14px rgba(37, 99, 235, 0.35);
}

.auth-title {
  font-size: 26px;
  font-weight: 800;
  color: white;
  margin-bottom: 4px;
}

.auth-subtitle {
  font-size: 14px;
  color: var(--slate-400);
}

/* Role Selector Bar */
.role-selector-bar {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 24px;
  padding: 10px 14px;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: var(--radius-md);
  flex-wrap: wrap;
}

.role-bar-label {
  font-size: 12px;
  font-weight: 600;
  color: var(--slate-400);
}

.role-pills-group {
  display: flex;
  gap: 6px;
}

.role-chip {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  background: rgba(255, 255, 255, 0.06);
  border: 1px solid rgba(255, 255, 255, 0.12);
  color: var(--slate-200);
  padding: 4px 10px;
  border-radius: var(--radius-full);
  font-size: 11.5px;
  font-weight: 600;
  cursor: pointer;
  transition: var(--transition-smooth);
}

.role-chip:hover {
  background: rgba(255, 255, 255, 0.15);
  color: white;
  transform: translateY(-1px);
}

.chip-admin:hover { border-color: #818cf8; color: #a5b4fc; }
.chip-doctor:hover { border-color: #38bdf8; color: #7dd3fc; }
.chip-patient:hover { border-color: #34d399; color: #6ee7b7; }

/* Form Fields */
.form-field-group {
  margin-bottom: 20px;
}

.label-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.form-label {
  display: block;
  font-size: 13px;
  font-weight: 600;
  color: var(--slate-300);
  margin-bottom: 6px;
}

.input-control-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.input-prefix-icon {
  position: absolute;
  left: 14px;
  font-size: 16px;
  color: var(--slate-400);
  pointer-events: none;
}

.saas-input {
  width: 100%;
  padding: 12px 14px 12px 42px;
  background: rgba(15, 23, 42, 0.6);
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: var(--radius-md);
  font-size: 14px;
  font-family: var(--font-primary);
  color: white;
  outline: none;
  transition: var(--transition-smooth);
}

.saas-input:focus {
  border-color: #38bdf8;
  background: rgba(15, 23, 42, 0.85);
  box-shadow: 0 0 0 3px rgba(56, 189, 248, 0.2);
}

.saas-input::placeholder {
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
  font-size: 16px;
}

.btn-toggle-password:hover {
  color: white;
}

/* Alert */
.saas-alert {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  padding: 12px 16px;
  border-radius: var(--radius-md);
  margin-bottom: 20px;
  font-size: 13px;
}

.saas-alert-danger {
  background: rgba(239, 68, 68, 0.15);
  border: 1px solid rgba(239, 68, 68, 0.35);
  color: #fca5a5;
}

.alert-icon {
  font-size: 16px;
  color: #ef4444;
  margin-top: 1px;
}

.alert-content {
  flex: 1;
}

.alert-dismiss {
  background: transparent;
  border: none;
  color: #fca5a5;
  cursor: pointer;
  font-size: 14px;
  padding: 0;
}

/* Submit Button */
.btn-auth-submit {
  width: 100%;
  padding: 13px;
  background: linear-gradient(135deg, #0284c7 0%, #2563eb 100%);
  color: white;
  border: none;
  border-radius: var(--radius-md);
  font-size: 15px;
  font-weight: 700;
  font-family: var(--font-primary);
  cursor: pointer;
  transition: var(--transition-smooth);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 14px rgba(37, 99, 235, 0.35);
  margin-top: 8px;
}

.btn-auth-submit:hover:not(:disabled) {
  background: linear-gradient(135deg, #0369a1 0%, #1d4ed8 100%);
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(37, 99, 235, 0.45);
}

.btn-auth-submit:disabled {
  opacity: 0.65;
  cursor: not-allowed;
}

/* Card Footer */
.auth-card-footer {
  margin-top: 28px;
  padding-top: 20px;
  border-top: 1px solid rgba(255, 255, 255, 0.08);
  text-align: center;
}

.auth-card-footer p {
  font-size: 13.5px;
  color: var(--slate-400);
  margin-bottom: 0;
}

.auth-link {
  color: #38bdf8;
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
@media (max-width: 880px) {
  .auth-layout-container {
    grid-template-columns: 1fr;
    max-width: 520px;
  }

  .auth-showcase-panel {
    display: none;
  }

  .auth-form-panel {
    padding: 36px 28px;
  }
}
</style>