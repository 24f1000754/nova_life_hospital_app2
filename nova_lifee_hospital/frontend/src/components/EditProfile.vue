<template>
  <div class="edit-profile-page">
    <div class="edit-profile-container">
      
      <!-- Header -->
      <div class="saas-card header-card">
        <div class="d-flex align-items-center gap-3">
          <button class="btn-back" @click="$router.push('/patient')" title="Return to Patient Portal">
            <i class="bi bi-arrow-left"></i>
          </button>
          <div>
            <div class="header-tag">ACCOUNT SETTINGS</div>
            <h2 class="header-title">Edit Patient Profile</h2>
            <p class="header-subtitle">Update your personal contact information and medical demographics.</p>
          </div>
        </div>
      </div>

      <!-- Form Card -->
      <div class="saas-card form-card">
        <form @submit.prevent="updateProfile">
          <!-- Full Name -->
          <div class="mb-3">
            <label class="saas-label">Full Name <span class="text-danger">*</span></label>
            <div class="input-icon-wrap">
              <i class="bi bi-person"></i>
              <input v-model="form.name" required class="saas-form-control" placeholder="Full name" />
            </div>
          </div>

          <!-- Age & Gender -->
          <div class="row g-3 mb-3">
            <div class="col-md-6">
              <label class="saas-label">Age (Years)</label>
              <div class="input-icon-wrap">
                <i class="bi bi-hourglass-split"></i>
                <input v-model="form.age" type="number" min="0" max="130" class="saas-form-control" placeholder="e.g. 32" />
              </div>
            </div>

            <div class="col-md-6">
              <label class="saas-label">Gender</label>
              <div class="input-icon-wrap">
                <i class="bi bi-gender-ambiguous"></i>
                <select v-model="form.gender" class="saas-form-select">
                  <option value="">Select gender</option>
                  <option value="Male">Male</option>
                  <option value="Female">Female</option>
                  <option value="Other">Other</option>
                </select>
              </div>
            </div>
          </div>

          <!-- Phone -->
          <div class="mb-4">
            <label class="saas-label">Contact Phone Number</label>
            <div class="input-icon-wrap">
              <i class="bi bi-telephone"></i>
              <input v-model="form.phone" type="tel" class="saas-form-control" placeholder="+1 (555) 019-2834" />
            </div>
          </div>

          <!-- Success Alert -->
          <div v-if="msg" class="saas-alert-success mb-3">
            <i class="bi bi-check-circle-fill me-2"></i>
            <span>{{ msg }}</span>
          </div>

          <div class="d-flex justify-content-end gap-2">
            <button type="button" class="btn-saas btn-saas-outline" @click="$router.push('/patient')">
              Cancel
            </button>
            <button type="submit" class="btn-saas btn-saas-primary" :disabled="saving">
              <span v-if="saving" class="spinner-border spinner-border-sm me-2"></span>
              <i v-else class="bi bi-check2-circle me-1"></i>
              <span>Save Changes</span>
            </button>
          </div>
        </form>
      </div>

    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'EditProfile',
  data() {
    return {
      user_id: localStorage.getItem('user_id'),
      form: {
        name: '',
        age: '',
        gender: '',
        phone: ''
      },
      msg: '',
      saving: false
    }
  },
  async mounted() {
    if (!this.user_id) return
    try {
      const res = await axios.get(`https://nova-life-hospital.onrender.com/api/patient/profile/${this.user_id}`)
      this.form = {
        name: res.data.name || '',
        age: res.data.age || '',
        gender: res.data.gender || '',
        phone: res.data.phone || ''
      }
    } catch (err) {
      console.error('Error loading patient profile:', err)
    }
  },
  methods: {
    async updateProfile() {
      this.saving = true
      this.msg = ''
      try {
        await axios.put(`https://nova-life-hospital.onrender.com/api/patient/profile/${this.user_id}`, this.form)
        this.msg = 'Profile updated successfully!'
        localStorage.setItem('name', this.form.name)
        // Dispatch storage event to sync header
        window.dispatchEvent(new Event('storage'))
      } catch (err) {
        alert(err.response?.data?.error || 'Failed to update profile')
      } finally {
        this.saving = false
      }
    }
  }
}
</script>

<style scoped>
.edit-profile-page {
  min-height: calc(100vh - 72px);
  background-color: var(--slate-100);
  padding: 36px 24px 60px;
}

.edit-profile-container {
  max-width: 680px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.header-card {
  background: white;
  border: 1px solid var(--slate-200);
  border-radius: var(--radius-xl);
  padding: 24px 30px;
  box-shadow: var(--shadow-sm);
}

.btn-back {
  width: 42px;
  height: 42px;
  border-radius: var(--radius-md);
  border: 1px solid var(--slate-300);
  background: var(--slate-50);
  color: var(--slate-700);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  cursor: pointer;
  transition: var(--transition-smooth);
  flex-shrink: 0;
}

.btn-back:hover {
  background: var(--slate-200);
  color: var(--slate-900);
}

.header-tag {
  font-size: 11px;
  font-weight: 700;
  color: var(--emerald-600);
  letter-spacing: 1px;
}

.header-title {
  font-size: 22px;
  font-weight: 800;
  color: var(--slate-900);
  margin: 2px 0;
}

.header-subtitle {
  font-size: 13.5px;
  color: var(--slate-500);
  margin-bottom: 0;
}

.form-card {
  background: white;
  border: 1px solid var(--slate-200);
  border-radius: var(--radius-xl);
  padding: 36px 40px;
  box-shadow: var(--shadow-sm);
}

.saas-label {
  display: block;
  font-size: 12.5px;
  font-weight: 600;
  color: var(--slate-700);
  margin-bottom: 6px;
}

.input-icon-wrap {
  position: relative;
  display: flex;
  align-items: center;
}

.input-icon-wrap i {
  position: absolute;
  left: 14px;
  font-size: 15px;
  color: var(--slate-400);
  pointer-events: none;
}

.saas-form-control,
.saas-form-select {
  width: 100%;
  padding: 10px 14px 10px 38px;
  background: var(--slate-50);
  border: 1px solid var(--slate-300);
  border-radius: var(--radius-md);
  font-size: 13.5px;
  font-family: var(--font-primary);
  color: var(--slate-800);
  outline: none;
  transition: var(--transition-smooth);
}

.saas-form-control:focus,
.saas-form-select:focus {
  border-color: #10b981;
  background: white;
  box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.15);
}

.saas-alert-success {
  display: flex;
  align-items: center;
  padding: 12px 16px;
  background: #ecfdf5;
  border: 1px solid #a7f3d0;
  border-radius: var(--radius-md);
  color: #065f46;
  font-size: 13.5px;
  font-weight: 600;
}

@media (max-width: 768px) {
  .form-card {
    padding: 24px 20px;
  }
}
</style>
