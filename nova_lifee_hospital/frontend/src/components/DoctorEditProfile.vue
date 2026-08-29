<template>
  <div class="edit-profile-page">
    <div class="edit-profile-container">
      
      <!-- Header -->
      <div class="saas-card header-card">
        <div class="d-flex align-items-center gap-3">
          <button class="btn-back" @click="$router.push('/doctor')" title="Return to Doctor Console">
            <i class="bi bi-arrow-left"></i>
          </button>
          <div>
            <div class="header-tag">SPECIALIST SETTINGS</div>
            <h2 class="header-title">Edit Physician Profile</h2>
            <p class="header-subtitle">Update your credentials, clinical specialization, bio, and hospital department address.</p>
          </div>
        </div>
      </div>

      <!-- Form Card -->
      <div class="saas-card form-card">
        <form @submit.prevent="save">
          <div class="row g-3 mb-3">
            <div class="col-md-6">
              <label class="saas-label">Doctor Full Name <span class="text-danger">*</span></label>
              <div class="input-icon-wrap">
                <i class="bi bi-person"></i>
                <input v-model="form.name" required class="saas-form-control" placeholder="Dr. Full Name" />
              </div>
            </div>

            <div class="col-md-6">
              <label class="saas-label">Official Email <span class="text-danger">*</span></label>
              <div class="input-icon-wrap">
                <i class="bi bi-envelope"></i>
                <input v-model="form.email" type="email" required class="saas-form-control" placeholder="doctor@hospital.com" />
              </div>
            </div>
          </div>

          <div class="row g-3 mb-3">
            <div class="col-md-4">
              <label class="saas-label">Clinical Specialization <span class="text-danger">*</span></label>
              <div class="input-icon-wrap">
                <i class="bi bi-tag"></i>
                <input v-model="form.specialization" required class="saas-form-control" placeholder="Cardiology, Neurology..." />
              </div>
            </div>

            <div class="col-md-4">
              <label class="saas-label">Gender</label>
              <div class="input-icon-wrap">
                <i class="bi bi-gender-ambiguous"></i>
                <input v-model="form.gender" class="saas-form-control" placeholder="Male / Female / Other" />
              </div>
            </div>

            <div class="col-md-4">
              <label class="saas-label">Experience</label>
              <div class="input-icon-wrap">
                <i class="bi bi-briefcase"></i>
                <input v-model="form.experience" class="saas-form-control" placeholder="e.g. 12 Years" />
              </div>
            </div>
          </div>

          <div class="row g-3 mb-3">
            <div class="col-md-6">
              <label class="saas-label">Education & Qualifications</label>
              <div class="input-icon-wrap">
                <i class="bi bi-mortarboard"></i>
                <input v-model="form.education" class="saas-form-control" placeholder="e.g. MBBS, MD, FRCP" />
              </div>
            </div>

            <div class="col-md-6">
              <label class="saas-label">Department / Clinic Address</label>
              <div class="input-icon-wrap">
                <i class="bi bi-geo-alt"></i>
                <input v-model="form.address" class="saas-form-control" placeholder="Block C, Level 2, Room 204" />
              </div>
            </div>
          </div>

          <div class="mb-4">
            <label class="saas-label">Professional Biography</label>
            <textarea v-model="form.bio" rows="4" class="saas-form-control" placeholder="Summarize your clinical focus, research interests, or hospital privileges..."></textarea>
          </div>

          <div class="d-flex justify-content-end gap-2">
            <button type="button" class="btn-saas btn-saas-outline" @click="$router.push('/doctor')">
              Cancel
            </button>
            <button type="submit" class="btn-saas btn-saas-primary" :disabled="saving">
              <span v-if="saving" class="spinner-border spinner-border-sm me-2"></span>
              <i v-else class="bi bi-check2-circle me-1"></i>
              <span>Save Profile Updates</span>
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
  name: 'DoctorEditProfile',
  data() {
    return {
      id: localStorage.getItem('user_id'),
      form: {
        name: '',
        email: '',
        gender: '',
        address: '',
        education: '',
        experience: '',
        specialization: '',
        bio: ''
      },
      saving: false
    }
  },
  async mounted() {
    if (!this.id) return
    try {
      const res = await axios.get(`http://127.0.0.1:5000/api/doctor/profile/${this.id}`)
      this.form = res.data || {}
    } catch (err) {
      console.error('Error fetching doctor profile:', err)
    }
  },
  methods: {
    async save() {
      this.saving = true
      try {
        await axios.put(`http://127.0.0.1:5000/api/doctor/update-profile/${this.id}`, this.form)
        alert('Profile updated successfully!')
        this.$router.push('/doctor')
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
  max-width: 860px;
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
  color: var(--teal-700);
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

.saas-form-control {
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

.saas-form-control:focus {
  border-color: var(--primary-500);
  background: white;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.15);
}

textarea.saas-form-control {
  padding-left: 14px;
  resize: vertical;
}

@media (max-width: 768px) {
  .form-card {
    padding: 24px 20px;
  }
}
</style>
