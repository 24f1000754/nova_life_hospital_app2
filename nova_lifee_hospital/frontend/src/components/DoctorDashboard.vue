<template>
  <div class="doctor-page">
    <div class="doctor-container">
      
      <!-- Top Operational Header Banner -->
      <div class="doctor-top-banner">
        <div class="banner-left">
          <div class="banner-badge">
            <i class="bi bi-heart-pulse-fill me-1"></i> SPECIALIST CLINICAL CONSOLE
          </div>
          <h1 class="banner-title">Dr. {{ profile.name || 'Specialist' }}</h1>
          <p class="banner-subtitle">
            <span class="spec-highlight">{{ profile.specialization || 'Clinical Specialist' }}</span>
            <span v-if="profile.education" class="text-muted ms-2">• {{ profile.education }}</span>
            <span v-if="profile.experience" class="text-muted ms-2">• {{ profile.experience }} Exp</span>
          </p>
        </div>
        <div class="banner-right">
          <button class="btn-banner-refresh" @click="load">
            <i class="bi bi-arrow-clockwise me-1"></i> Refresh Schedule
          </button>
        </div>
      </div>

      <!-- Doctor Information Card (View / Inline Edit) -->
      <div class="saas-card profile-card">
        <div class="saas-card-header">
          <div class="d-flex align-items-center gap-3">
            <div class="user-avatar avatar-doctor-lg">
              {{ getInitials(profile.name) }}
            </div>
            <div>
              <h4 class="saas-card-title">Physician Profile & Credentials</h4>
              <p class="saas-card-subtitle">Public details visible to patients during appointment scheduling</p>
            </div>
          </div>
          <button v-if="!editing" class="btn-saas btn-saas-outline" @click="openEdit">
            <i class="bi bi-pencil me-1"></i> Edit Profile
          </button>
        </div>

        <div class="saas-card-body">
          <!-- View Mode -->
          <div v-if="!editing" class="profile-details-grid">
            <div class="pdetail-item">
              <span class="pdetail-label">Full Name</span>
              <span class="pdetail-value">Dr. {{ profile.name || 'N/A' }}</span>
            </div>

            <div class="pdetail-item">
              <span class="pdetail-label">Email Address</span>
              <span class="pdetail-value">{{ profile.email || 'N/A' }}</span>
            </div>

            <div class="pdetail-item">
              <span class="pdetail-label">Clinical Specialization</span>
              <span class="pdetail-value text-primary">{{ profile.specialization || 'General Practice' }}</span>
            </div>

            <div class="pdetail-item">
              <span class="pdetail-label">Gender</span>
              <span class="pdetail-value">{{ profile.gender || 'Not specified' }}</span>
            </div>

            <div class="pdetail-item">
              <span class="pdetail-label">Education / Degrees</span>
              <span class="pdetail-value">{{ profile.education || 'N/A' }}</span>
            </div>

            <div class="pdetail-item">
              <span class="pdetail-label">Clinical Experience</span>
              <span class="pdetail-value">{{ profile.experience || 'N/A' }}</span>
            </div>

            <div class="pdetail-item full-width">
              <span class="pdetail-label">Professional Biography</span>
              <div class="pdetail-bio">{{ profile.bio || 'No medical biography added yet.' }}</div>
            </div>

            <div class="pdetail-item full-width">
              <span class="pdetail-label">Clinic / Hospital Department Address</span>
              <span class="pdetail-value">{{ profile.address || 'N/A' }}</span>
            </div>
          </div>

          <!-- Edit Mode Form -->
          <div v-else class="profile-edit-form">
            <div class="row g-3 mb-3">
              <div class="col-md-6">
                <label class="saas-label">Name</label>
                <input v-model="form.name" class="saas-form-control" />
              </div>
              <div class="col-md-6">
                <label class="saas-label">Email</label>
                <input v-model="form.email" type="email" class="saas-form-control" />
              </div>
            </div>

            <div class="row g-3 mb-3">
              <div class="col-md-4">
                <label class="saas-label">Specialization</label>
                <input v-model="form.specialization" class="saas-form-control" />
              </div>
              <div class="col-md-4">
                <label class="saas-label">Gender</label>
                <input v-model="form.gender" class="saas-form-control" placeholder="Male / Female / Other" />
              </div>
              <div class="col-md-4">
                <label class="saas-label">Experience</label>
                <input v-model="form.experience" class="saas-form-control" placeholder="e.g. 10 years" />
              </div>
            </div>

            <div class="row g-3 mb-3">
              <div class="col-md-6">
                <label class="saas-label">Education / Medical Degrees</label>
                <input v-model="form.education" class="saas-form-control" placeholder="e.g. MBBS, MD (Cardiology)" />
              </div>
              <div class="col-md-6">
                <label class="saas-label">Department Address</label>
                <input v-model="form.address" class="saas-form-control" placeholder="Wing B, Room 304" />
              </div>
            </div>

            <div class="mb-3">
              <label class="saas-label">Professional Biography</label>
              <textarea v-model="form.bio" rows="3" class="saas-form-control"></textarea>
            </div>

            <div class="d-flex justify-content-end gap-2">
              <button class="btn-saas btn-saas-outline" @click="editing = false">Cancel</button>
              <button class="btn-saas btn-saas-primary" @click="save">Save Profile Changes</button>
            </div>
          </div>
        </div>
      </div>

      <!-- Clinical KPI Stats Grid (5 Cards) -->
      <div class="stats-grid-5">
        <div class="kpi-mini-card kpi-today">
          <div class="kpi-mini-icon"><i class="bi bi-calendar-event"></i></div>
          <div>
            <span class="kpi-mini-label">Today's Visits</span>
            <h3 class="kpi-mini-value">{{ stats.today ?? 0 }}</h3>
          </div>
        </div>

        <div class="kpi-mini-card kpi-total">
          <div class="kpi-mini-icon"><i class="bi bi-calendar2-range"></i></div>
          <div>
            <span class="kpi-mini-label">Total Visits</span>
            <h3 class="kpi-mini-value">{{ stats.total ?? 0 }}</h3>
          </div>
        </div>

        <div class="kpi-mini-card kpi-pending">
          <div class="kpi-mini-icon"><i class="bi bi-clock-history"></i></div>
          <div>
            <span class="kpi-mini-label">Pending</span>
            <h3 class="kpi-mini-value">{{ stats.pending ?? 0 }}</h3>
          </div>
        </div>

        <div class="kpi-mini-card kpi-completed">
          <div class="kpi-mini-icon"><i class="bi bi-check2-all"></i></div>
          <div>
            <span class="kpi-mini-label">Completed</span>
            <h3 class="kpi-mini-value">{{ stats.completed ?? 0 }}</h3>
          </div>
        </div>

        <div class="kpi-mini-card kpi-patients">
          <div class="kpi-mini-icon"><i class="bi bi-people"></i></div>
          <div>
            <span class="kpi-mini-label">Patients</span>
            <h3 class="kpi-mini-value">{{ stats.patients ?? 0 }}</h3>
          </div>
        </div>
      </div>

      <!-- Add Consultation Availability Widget -->
      <div class="saas-card slot-widget-card">
        <div class="saas-card-header">
          <div class="d-flex align-items-center gap-2">
            <i class="bi bi-calendar-plus text-primary fs-5"></i>
            <h4 class="saas-card-title">Add Availability Slot</h4>
          </div>
          <span class="text-muted small">Slots become immediately available for patient booking</span>
        </div>

        <div class="saas-card-body">
          <div class="row g-3 align-items-end">
            <div class="col-md-5">
              <label class="saas-label">Consultation Date</label>
              <input type="date" v-model="slot.date" class="saas-form-control" :min="todayDateStr" />
            </div>

            <div class="col-md-4">
              <label class="saas-label">Time Slot</label>
              <input type="time" v-model="slot.time" class="saas-form-control" />
            </div>

            <div class="col-md-3">
              <button class="btn-saas btn-saas-primary w-100" @click="addSlot" :disabled="!slot.date || !slot.time">
                <i class="bi bi-plus-circle me-1"></i> Publish Slot
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Upcoming Appointments Table -->
      <div class="saas-card table-section-card">
        <div class="table-card-header">
          <div class="table-header-left">
            <h4 class="saas-card-title">Upcoming Patient Consultations</h4>
            <span class="badge-counter">{{ upcomingAppointments.length }} Pending</span>
          </div>
        </div>

        <div class="saas-table-wrapper">
          <table class="saas-table">
            <thead>
              <tr>
                <th>Patient Name</th>
                <th>Consultation Date</th>
                <th>Scheduled Time</th>
                <th>Status</th>
                <th class="text-end">Clinical Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="a in upcomingAppointments" :key="a.id">
                <td>
                  <div class="user-cell">
                    <div class="user-avatar-sm avatar-patient">
                      {{ getInitials(a.patient) }}
                    </div>
                    <div class="user-cell-meta">
                      <span class="cell-primary-text">{{ a.patient }}</span>
                      <span class="cell-secondary-text">Appointment #{{ a.id }}</span>
                    </div>
                  </div>
                </td>
                <td>
                  <span class="date-badge"><i class="bi bi-calendar3 me-1"></i>{{ a.date }}</span>
                </td>
                <td>
                  <span class="time-badge"><i class="bi bi-clock me-1"></i>{{ formatTime(a.time) }}</span>
                </td>
                <td>
                  <span class="status-pill pill-warning">
                    <span class="pulse-dot"></span>
                    {{ a.status }}
                  </span>
                </td>
                <td class="text-end">
                  <div class="table-action-btns">
                    <button class="btn-table-action btn-action-success" @click="complete(a.id)" title="Mark Consultation Completed">
                      <i class="bi bi-check-lg"></i> Complete
                    </button>
                    <button class="btn-table-action btn-action-treatment" @click="goToTreatment(a.id)" title="Write Prescription / Diagnosis">
                      <i class="bi bi-file-earmark-medical-fill"></i> Add Treatment
                    </button>
                    <button class="btn-table-action btn-action-delete" @click="cancel(a.id)" title="Cancel Consultation">
                      <i class="bi bi-x-lg"></i> Cancel
                    </button>
                  </div>
                </td>
              </tr>
              <tr v-if="upcomingAppointments.length === 0">
                <td colspan="5" class="table-empty-message">
                  <i class="bi bi-calendar-check fs-4 d-block mb-2 text-muted"></i>
                  No upcoming appointments scheduled.
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Clinical Appointment History Table -->
      <div class="saas-card table-section-card">
        <div class="table-card-header">
          <div class="table-header-left">
            <h4 class="saas-card-title">Consultation History & Prescriptions</h4>
            <span class="badge-counter badge-counter-teal">{{ appointmentHistory.length }} Records</span>
          </div>
        </div>

        <div class="saas-table-wrapper">
          <table class="saas-table">
            <thead>
              <tr>
                <th>Patient</th>
                <th>Date & Time</th>
                <th>Status</th>
                <th>Diagnosis Summary</th>
                <th>Prescription & Treatment</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="a in appointmentHistory" :key="a.id">
                <td>
                  <div class="user-cell">
                    <div class="user-avatar-sm avatar-patient">
                      {{ getInitials(a.patient) }}
                    </div>
                    <span class="cell-primary-text">{{ a.patient }}</span>
                  </div>
                </td>
                <td>
                  <div>
                    <span class="date-badge"><i class="bi bi-calendar3 me-1"></i>{{ a.date }}</span>
                    <div class="time-badge mt-1"><i class="bi bi-clock me-1"></i>{{ formatTime(a.time) }}</div>
                  </div>
                </td>
                <td>
                  <span :class="a.status === 'Completed' ? 'status-pill pill-success' : 'status-pill pill-danger'">
                    <span class="pulse-dot"></span>
                    {{ a.status }}
                  </span>
                </td>
                <td>
                  <div class="diagnosis-snippet">
                    {{ a.diagnosis || '—' }}
                  </div>
                </td>
                <td>
                  <div class="prescription-snippet">
                    {{ a.prescription || '—' }}
                  </div>
                </td>
              </tr>
              <tr v-if="appointmentHistory.length === 0">
                <td colspan="5" class="table-empty-message">No past consultation records found.</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Assigned Patients Directory -->
      <div class="saas-card table-section-card">
        <div class="table-card-header">
          <div class="table-header-left">
            <h4 class="saas-card-title">Assigned Patients Directory</h4>
            <span class="badge-counter badge-counter-indigo">{{ patients.length }} Patients</span>
          </div>
        </div>

        <div class="saas-table-wrapper">
          <table class="saas-table">
            <thead>
              <tr>
                <th>Patient Name</th>
                <th>Email Address</th>
                <th>Contact Phone</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="p in patients" :key="p.id">
                <td>
                  <div class="user-cell">
                    <div class="user-avatar-sm avatar-patient">
                      {{ getInitials(p.name) }}
                    </div>
                    <span class="cell-primary-text">{{ p.name }}</span>
                  </div>
                </td>
                <td><span class="cell-primary-text">{{ p.email }}</span></td>
                <td>
                  <span v-if="p.phone" class="phone-pill"><i class="bi bi-telephone me-1"></i>{{ p.phone }}</span>
                  <span v-else class="text-muted">N/A</span>
                </td>
              </tr>
              <tr v-if="patients.length === 0">
                <td colspan="3" class="table-empty-message">No patients have booked appointments with you yet.</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'DoctorDashboard',
  data() {
    return {
      userId: localStorage.getItem('user_id'),
      profile: {},
      stats: {},
      appointments: [],
      patients: [],
      slot: { date: '', time: '' },
      editing: false,
      form: {}
    }
  },
  computed: {
    todayDateStr() {
      return new Date().toISOString().split('T')[0]
    },
    upcomingAppointments() {
      return this.appointments.filter(a => a.status === 'Booked')
    },
    appointmentHistory() {
      return this.appointments.filter(a => a.status !== 'Booked')
    }
  },
  async mounted() {
    await this.load()
  },
  methods: {
    getInitials(name) {
      if (!name) return 'U'
      return name
        .split(' ')
        .map(n => n[0])
        .join('')
        .toUpperCase()
        .slice(0, 2)
    },
    formatTime(t) {
      if (!t) return ''
      try {
        const [h, m] = t.split(':')
        const hr = parseInt(h)
        return `${hr % 12 || 12}:${m} ${hr >= 12 ? 'PM' : 'AM'}`
      } catch {
        return t
      }
    },
    async load() {
      if (!this.userId) return
      try {
        const [profRes, statsRes, appRes, patRes] = await Promise.all([
          axios.get(`http://127.0.0.1:5000/api/doctor/profile/${this.userId}`),
          axios.get(`http://127.0.0.1:5000/api/doctor/stats/${this.userId}`),
          axios.get(`http://127.0.0.1:5000/api/doctor/appointments/${this.userId}`),
          axios.get(`http://127.0.0.1:5000/api/doctor/patients/${this.userId}`)
        ])

        this.profile = profRes.data || {}
        this.form = { ...this.profile }
        this.stats = statsRes.data || {}
        this.appointments = appRes.data?.data || []
        this.patients = patRes.data?.data || []
      } catch (err) {
        console.error('Error loading doctor data:', err)
      }
    },
    openEdit() {
      this.form = { ...this.profile }
      this.editing = true
    },
    async save() {
      try {
        await axios.put(`http://127.0.0.1:5000/api/doctor/update-profile/${this.userId}`, this.form)
        alert('Profile updated successfully!')
        this.editing = false
        await this.load()
      } catch (err) {
        alert(err.response?.data?.error || 'Failed to update doctor profile')
      }
    },
    async addSlot() {
      if (!this.slot.date || !this.slot.time) return
      try {
        await axios.post('http://127.0.0.1:5000/api/doctor/add-availability', {
          doctor_id: this.userId,
          date: this.slot.date,
          time: this.slot.time
        })
        alert('Availability slot published successfully!')
        this.slot = { date: '', time: '' }
        await this.load()
      } catch (err) {
        alert(err.response?.data?.error || 'Failed to add availability slot')
      }
    },
    async complete(id) {
      try {
        await axios.put('http://127.0.0.1:5000/api/doctor/update-status', {
          appointment_id: id,
          status: 'Completed'
        })
        await this.load()
      } catch (err) {
        alert('Failed to mark appointment completed')
      }
    },
    goToTreatment(id) {
      this.$router.push(`/doctor/treatment/${id}`)
    },
    async cancel(id) {
      if (!confirm('Are you sure you want to cancel this appointment?')) return
      try {
        await axios.put('http://127.0.0.1:5000/api/doctor/update-status', {
          appointment_id: id,
          status: 'Cancelled'
        })
        alert('Appointment marked as cancelled.')
        await this.load()
      } catch (err) {
        alert('Failed to cancel appointment')
      }
    },
    logout() {
      localStorage.clear()
      this.$router.push('/login')
    }
  }
}
</script>

<style scoped>
.doctor-page {
  min-height: calc(100vh - 72px);
  background-color: var(--slate-100);
  padding: 36px 28px 60px;
}

.doctor-container {
  max-width: 1440px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 26px;
}

/* ==========================================================================
   HEADER BANNER
   ========================================================================== */
.doctor-top-banner {
  background: white;
  border: 1px solid var(--slate-200);
  border-radius: var(--radius-xl);
  padding: 32px 36px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  box-shadow: var(--shadow-sm);
  gap: 20px;
  flex-wrap: wrap;
}

.banner-badge {
  display: inline-flex;
  align-items: center;
  font-size: 11px;
  font-weight: 700;
  color: var(--teal-700);
  background: var(--teal-50);
  border: 1px solid rgba(20, 184, 166, 0.3);
  padding: 5px 12px;
  border-radius: var(--radius-full);
  letter-spacing: 0.8px;
  margin-bottom: 8px;
}

.banner-title {
  font-size: 28px;
  font-weight: 800;
  color: var(--slate-900);
  margin-bottom: 4px;
}

.spec-highlight {
  color: var(--primary-600);
  font-weight: 700;
  font-size: 15px;
}

.banner-subtitle {
  font-size: 14px;
  margin-bottom: 0;
}

.btn-banner-refresh {
  display: inline-flex;
  align-items: center;
  padding: 10px 20px;
  background: var(--slate-50);
  border: 1px solid var(--slate-300);
  border-radius: var(--radius-md);
  font-size: 13.5px;
  font-weight: 600;
  color: var(--slate-700);
  cursor: pointer;
  transition: var(--transition-smooth);
}

.btn-banner-refresh:hover {
  background: var(--slate-100);
  color: var(--slate-900);
}

/* ==========================================================================
   PROFILE CARD
   ========================================================================== */
.profile-card {
  background: white;
  border: 1px solid var(--slate-200);
  border-radius: var(--radius-xl);
  padding: 28px 32px;
  box-shadow: var(--shadow-sm);
}

.avatar-doctor-lg {
  width: 52px;
  height: 52px;
  border-radius: var(--radius-lg);
  font-size: 18px;
}

.profile-details-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
}

.pdetail-item {
  display: flex;
  flex-direction: column;
}

.pdetail-item.full-width {
  grid-column: 1 / -1;
}

.pdetail-label {
  font-size: 12px;
  font-weight: 600;
  color: var(--slate-500);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 3px;
}

.pdetail-value {
  font-size: 14.5px;
  font-weight: 600;
  color: var(--slate-800);
}

.pdetail-bio {
  background: var(--slate-50);
  border: 1px solid var(--slate-200);
  padding: 14px;
  border-radius: var(--radius-md);
  font-size: 13.5px;
  color: var(--slate-700);
  line-height: 1.6;
}

/* ==========================================================================
   5-METRIC STATS GRID
   ========================================================================== */
.stats-grid-5 {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 16px;
}

.kpi-mini-card {
  background: white;
  border: 1px solid var(--slate-200);
  border-radius: var(--radius-lg);
  padding: 18px 20px;
  display: flex;
  align-items: center;
  gap: 14px;
  box-shadow: var(--shadow-sm);
  transition: var(--transition-smooth);
}

.kpi-mini-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

.kpi-mini-icon {
  width: 44px;
  height: 44px;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  flex-shrink: 0;
}

.kpi-today .kpi-mini-icon { background: var(--primary-50); color: var(--primary-600); }
.kpi-total .kpi-mini-icon { background: var(--teal-50); color: var(--teal-600); }
.kpi-pending .kpi-mini-icon { background: #fef3c7; color: #d97706; }
.kpi-completed .kpi-mini-icon { background: #d1fae5; color: #059669; }
.kpi-patients .kpi-mini-icon { background: #e0e7ff; color: #4f46e5; }

.kpi-mini-label {
  display: block;
  font-size: 12px;
  font-weight: 600;
  color: var(--slate-500);
  text-transform: uppercase;
}

.kpi-mini-value {
  font-size: 24px;
  font-weight: 800;
  color: var(--slate-900);
  line-height: 1.1;
  margin: 2px 0 0;
}

/* ==========================================================================
   SLOT WIDGET CARD
   ========================================================================== */
.slot-widget-card {
  background: white;
  border: 1px solid var(--slate-200);
  border-radius: var(--radius-xl);
  padding: 24px 30px;
  box-shadow: var(--shadow-sm);
}

/* ==========================================================================
   DATA TABLES
   ========================================================================== */
.table-section-card {
  background: white;
  border: 1px solid var(--slate-200);
  border-radius: var(--radius-xl);
  padding: 26px 30px;
  box-shadow: var(--shadow-sm);
}

.table-card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
}

.table-header-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.badge-counter {
  font-size: 12px;
  font-weight: 700;
  color: var(--primary-700);
  background: var(--primary-50);
  padding: 4px 10px;
  border-radius: var(--radius-full);
}

.badge-counter-teal { color: var(--teal-700); background: var(--teal-50); }
.badge-counter-indigo { color: #4338ca; background: #e0e7ff; }

.saas-table-wrapper {
  overflow-x: auto;
  border: 1px solid var(--slate-200);
  border-radius: var(--radius-lg);
}

.saas-table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
}

.saas-table th {
  background: var(--slate-50);
  color: var(--slate-600);
  font-size: 12px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.6px;
  padding: 14px 18px;
  border-bottom: 1px solid var(--slate-200);
}

.saas-table td {
  padding: 14px 18px;
  border-bottom: 1px solid var(--slate-100);
  font-size: 13.5px;
  color: var(--slate-800);
  vertical-align: middle;
}

.saas-table tbody tr:hover {
  background-color: var(--slate-50);
}

.user-cell {
  display: flex;
  align-items: center;
  gap: 12px;
}

.user-avatar-sm {
  width: 34px;
  height: 34px;
  border-radius: var(--radius-full);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12.5px;
  font-weight: 800;
  color: white;
  flex-shrink: 0;
}

.user-cell-meta {
  display: flex;
  flex-direction: column;
}

.cell-primary-text { font-weight: 600; color: var(--slate-900); }
.cell-secondary-text { font-size: 12px; color: var(--slate-500); }

.status-pill {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 4px 10px;
  border-radius: var(--radius-full);
  font-size: 12px;
  font-weight: 700;
}

.pill-success { background: #d1fae5; color: #065f46; }
.pill-danger { background: #fee2e2; color: #991b1b; }
.pill-warning { background: #fef3c7; color: #92400e; }

.date-badge, .time-badge {
  font-size: 12.5px;
  color: var(--slate-700);
}

.phone-pill {
  font-size: 12.5px;
  color: var(--slate-700);
  background: var(--slate-100);
  padding: 3px 8px;
  border-radius: 4px;
}

/* Action Buttons */
.table-action-btns {
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

.btn-table-action {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 6px 12px;
  font-size: 12px;
  font-weight: 600;
  border-radius: var(--radius-sm);
  border: 1px solid transparent;
  cursor: pointer;
  transition: var(--transition-smooth);
}

.btn-action-success {
  background: #ecfdf5;
  color: #047857;
  border-color: #a7f3d0;
}

.btn-action-success:hover {
  background: #047857;
  color: white;
}

.btn-action-treatment {
  background: #eff6ff;
  color: var(--primary-600);
  border-color: var(--primary-200);
}

.btn-action-treatment:hover {
  background: var(--primary-600);
  color: white;
}

.btn-action-delete {
  background: #fef2f2;
  color: #dc2626;
  border-color: #fee2e2;
}

.btn-action-delete:hover {
  background: #dc2626;
  color: white;
}

.diagnosis-snippet, .prescription-snippet {
  max-width: 260px;
  font-size: 13px;
  color: var(--slate-700);
  line-height: 1.4;
  white-space: pre-wrap;
}

.table-empty-message {
  text-align: center;
  padding: 36px;
  color: var(--slate-400);
  font-size: 14px;
}

/* ==========================================================================
   RESPONSIVENESS
   ========================================================================== */
@media (max-width: 1200px) {
  .stats-grid-5 {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 900px) {
  .profile-details-grid {
    grid-template-columns: 1fr;
  }

  .stats-grid-5 {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .doctor-page {
    padding: 20px 14px;
  }
}
</style>