<template>
  <div class="patient-page">
    <div class="patient-container">
      
      <!-- Top Welcome Banner -->
      <div class="patient-top-banner">
        <div class="banner-user-info">
          <div class="user-avatar avatar-patient-lg">
            {{ getInitials(patientName) }}
          </div>
          <div>
            <div class="banner-tag">PATIENT HEALTH PORTAL</div>
            <h1 class="banner-title">Welcome, {{ patientName }}</h1>
            <p class="banner-subtitle">Manage specialist consultations, check weekly clinic schedules, and download clinical records.</p>
          </div>
        </div>

        <div class="banner-actions">
          <button class="btn-saas btn-saas-outline" @click="$router.push('/edit-profile')">
            <i class="bi bi-person-gear me-1"></i> Edit Profile
          </button>
          <a href="#book-section" class="btn-saas btn-saas-primary">
            <i class="bi bi-calendar-plus me-1"></i> Book Specialist
          </a>
        </div>
      </div>

      <!-- Personal Info & Medical Profile Summary Card -->
      <div class="saas-card info-summary-card">
        <div class="card-title-group">
          <i class="bi bi-person-lines-fill text-primary fs-5"></i>
          <h4 class="saas-card-title">Personal Demographic Information</h4>
        </div>

        <div class="info-pills-grid">
          <div class="info-box">
            <span class="info-label"><i class="bi bi-person me-1"></i> Full Name</span>
            <span class="info-val">{{ profile.name || patientName || 'Not Set' }}</span>
          </div>

          <div class="info-box">
            <span class="info-label"><i class="bi bi-envelope me-1"></i> Email Address</span>
            <span class="info-val">{{ profile.email || 'Not Set' }}</span>
          </div>

          <div class="info-box">
            <span class="info-label"><i class="bi bi-telephone me-1"></i> Phone</span>
            <span class="info-val">{{ profile.phone || 'Not Set' }}</span>
          </div>

          <div class="info-box">
            <span class="info-label"><i class="bi bi-hourglass-split me-1"></i> Age</span>
            <span class="info-val">{{ profile.age ? `${profile.age} Years` : 'Not Set' }}</span>
          </div>

          <div class="info-box">
            <span class="info-label"><i class="bi bi-gender-ambiguous me-1"></i> Gender</span>
            <span class="info-val">{{ profile.gender || 'Not Set' }}</span>
          </div>

          <div class="info-box full-width">
            <span class="info-label"><i class="bi bi-geo-alt me-1"></i> Residential Address</span>
            <span class="info-val">{{ profile.address || 'No residential address recorded.' }}</span>
          </div>
        </div>
      </div>

      <!-- KPI Metric Cards Grid -->
      <div class="stats-grid">
        <div class="kpi-card kpi-upcoming">
          <div class="kpi-icon-wrap">
            <i class="bi bi-clock-history"></i>
          </div>
          <div class="kpi-body">
            <span class="kpi-label">Upcoming Visits</span>
            <h2 class="kpi-value">{{ stats[0]?.value ?? 0 }}</h2>
            <span class="kpi-meta"><i class="bi bi-calendar-check text-primary me-1"></i>Confirmed Appointments</span>
          </div>
        </div>

        <div class="kpi-card kpi-total">
          <div class="kpi-icon-wrap">
            <i class="bi bi-calendar-range"></i>
          </div>
          <div class="kpi-body">
            <span class="kpi-label">Total Visits</span>
            <h2 class="kpi-value">{{ stats[1]?.value ?? 0 }}</h2>
            <span class="kpi-meta"><i class="bi bi-clipboard2-check text-success me-1"></i>Consultation Records</span>
          </div>
        </div>

        <div class="kpi-card kpi-doctors">
          <div class="kpi-icon-wrap">
            <i class="bi bi-people-fill"></i>
          </div>
          <div class="kpi-body">
            <span class="kpi-label">Specialists Consulted</span>
            <h2 class="kpi-value">{{ stats[2]?.value ?? 0 }}</h2>
            <span class="kpi-meta"><i class="bi bi-heart-pulse text-warning me-1"></i>Clinical Specialists</span>
          </div>
        </div>
      </div>

      <!-- 7-Day Specialist Availability Calendar Matrix -->
      <div class="saas-card table-section-card">
        <div class="table-card-header">
          <div class="table-header-left">
            <h4 class="saas-card-title">Doctor Availability Schedule (Next 7 Days)</h4>
            <span class="badge-counter">Weekly Outlook</span>
          </div>
          <span class="text-muted small">Live clinic consultation slots across departments</span>
        </div>

        <div class="availability-matrix-wrapper">
          <table class="matrix-table">
            <thead>
              <tr>
                <th class="matrix-doctor-th">Physician</th>
                <th class="matrix-spec-th">Department</th>
                <th v-for="(date, idx) in availabilityDates" :key="idx" class="matrix-date-th">
                  <div class="matrix-date-header">
                    <span class="matrix-day">{{ getDayName(date) }}</span>
                    <span class="matrix-cal-date">{{ getFormattedDayDate(date) }}</span>
                  </div>
                </th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="doc in doctorAvailability" :key="doc.doctor_name">
                <td class="matrix-doc-name-cell">
                  <div class="user-cell">
                    <div class="user-avatar-sm avatar-doctor">
                      {{ getInitials(doc.doctor_name) }}
                    </div>
                    <span class="cell-primary-text">Dr. {{ doc.doctor_name }}</span>
                  </div>
                </td>
                <td>
                  <span class="spec-pill">{{ doc.specialization || 'General Practice' }}</span>
                </td>
                <td v-for="(slot, idx) in doc.availability" :key="idx" class="matrix-slot-cell">
                  <span v-if="slot.available" class="matrix-chip chip-available">
                    <i class="bi bi-check-circle-fill me-1"></i> Available
                  </span>
                  <span v-else class="matrix-chip chip-unavailable">
                    —
                  </span>
                </td>
              </tr>
              <tr v-if="doctorAvailability.length === 0">
                <td :colspan="availabilityDates.length + 2" class="table-empty-message">
                  Loading 7-day doctor availability calendar...
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Book an Appointment Section -->
      <div id="book-section" class="saas-card booking-card">
        <div class="table-card-header">
          <div class="table-header-left">
            <h4 class="saas-card-title">Schedule a Specialist Consultation</h4>
            <span class="badge-counter badge-counter-teal">Instant Booking</span>
          </div>

          <!-- Specialization Filter Dropdown -->
          <div class="booking-filter-wrapper">
            <select v-model="filter" class="saas-form-select filter-select">
              <option value="">All Clinical Specializations</option>
              <option v-for="s in specializations" :key="s" :value="s">{{ s }}</option>
            </select>
          </div>
        </div>

        <!-- Doctors Grid -->
        <div class="doctors-cards-grid">
          <div class="doctor-booking-card" v-for="d in filteredDoctors" :key="d.id">
            <div class="doc-card-top">
              <div class="user-avatar avatar-doctor">
                {{ getInitials(d.name) }}
              </div>
              <div class="doc-card-info">
                <h5 class="doc-card-name">Dr. {{ d.name }}</h5>
                <span class="spec-pill">{{ d.specialization || 'Specialist' }}</span>
              </div>
            </div>

            <div class="doc-card-body">
              <label class="saas-label">Select Consultation Slot</label>
              <div class="slot-select-wrapper">
                <select class="saas-form-select" v-model="d.selectedSlot" @click="loadSlots(d)">
                  <option disabled value="">Choose Date & Time...</option>
                  <option v-for="s in d.slots" :key="s.id" :value="s">
                    {{ s.date }} | {{ formatTime(s.time) }}
                  </option>
                </select>
              </div>

              <button class="btn-saas btn-saas-primary w-100 mt-3" @click="book(d)">
                <i class="bi bi-calendar-check me-1"></i> Book Appointment
              </button>
            </div>
          </div>
        </div>

        <div v-if="filteredDoctors.length === 0" class="table-empty-message">
          No medical specialists found matching the selected filter.
        </div>
      </div>

      <!-- Upcoming Appointments Table -->
      <div class="saas-card table-section-card">
        <div class="table-card-header">
          <div class="table-header-left">
            <h4 class="saas-card-title">Your Upcoming Appointments</h4>
            <span class="badge-counter">{{ upcomingAppointments.length }} Active</span>
          </div>
        </div>

        <div class="saas-table-wrapper">
          <table class="saas-table">
            <thead>
              <tr>
                <th>Attending Doctor</th>
                <th>Specialization</th>
                <th>Appointment Date</th>
                <th>Time Slot</th>
                <th>Status</th>
                <th class="text-end">Action</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="a in upcomingAppointments" :key="a.id">
                <td>
                  <div class="user-cell">
                    <div class="user-avatar-sm avatar-doctor">{{ getInitials(a.doctor) }}</div>
                    <span class="cell-primary-text">Dr. {{ a.doctor }}</span>
                  </div>
                </td>
                <td><span class="spec-pill">{{ a.specialization }}</span></td>
                <td><span class="date-badge"><i class="bi bi-calendar3 me-1"></i>{{ a.date }}</span></td>
                <td><span class="time-badge"><i class="bi bi-clock me-1"></i>{{ formatTime(a.time) }}</span></td>
                <td>
                  <span class="status-pill pill-warning">
                    <span class="pulse-dot"></span> Booked
                  </span>
                </td>
                <td class="text-end">
                  <button class="btn-table-action btn-action-delete" @click="cancelAppointment(a.id)">
                    <i class="bi bi-x-circle me-1"></i> Cancel
                  </button>
                </td>
              </tr>
              <tr v-if="upcomingAppointments.length === 0">
                <td colspan="6" class="table-empty-message">You have no upcoming appointments scheduled.</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Appointment History & Treatment Review Table -->
      <div class="saas-card table-section-card">
        <div class="table-card-header">
          <div class="table-header-left">
            <h4 class="saas-card-title">Consultation History & Medical Prescriptions</h4>
            <span class="badge-counter badge-counter-teal">{{ pastAppointments.length }} Past Visits</span>
          </div>
        </div>

        <div class="saas-table-wrapper">
          <table class="saas-table">
            <thead>
              <tr>
                <th>Attending Doctor</th>
                <th>Specialization</th>
                <th>Date</th>
                <th>Time</th>
                <th>Status</th>
                <th class="text-end">Treatment Record</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="a in pastAppointments" :key="a.id">
                <td>
                  <div class="user-cell">
                    <div class="user-avatar-sm avatar-doctor">{{ getInitials(a.doctor) }}</div>
                    <span class="cell-primary-text">Dr. {{ a.doctor }}</span>
                  </div>
                </td>
                <td><span class="spec-pill">{{ a.specialization }}</span></td>
                <td><span class="date-badge">{{ a.date }}</span></td>
                <td><span class="time-badge">{{ formatTime(a.time) }}</span></td>
                <td>
                  <span :class="a.status === 'Completed' ? 'status-pill pill-success' : 'status-pill pill-danger'">
                    <span class="pulse-dot"></span> {{ a.status }}
                  </span>
                </td>
                <td class="text-end">
                  <button v-if="a.status === 'Completed'" class="btn-table-action btn-action-view" @click="viewTreatment(a.id)">
                    <i class="bi bi-file-earmark-medical me-1"></i> View Prescription
                  </button>
                  <span v-else class="text-muted small">No record</span>
                </td>
              </tr>
              <tr v-if="pastAppointments.length === 0">
                <td colspan="6" class="table-empty-message">No past appointment history recorded.</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Export Treatment Report Widget (Celery Async CSV) -->
      <div class="saas-card export-card">
        <div class="d-flex align-items-center gap-3">
          <div class="export-icon-circle">
            <i class="bi bi-file-earmark-spreadsheet-fill"></i>
          </div>
          <div>
            <h4 class="saas-card-title">Export Comprehensive Treatment Report</h4>
            <p class="saas-card-subtitle">Generate and download a certified CSV file summarizing all your completed clinical appointments and prescriptions.</p>
          </div>
        </div>

        <div class="export-controls-row">
          <div class="btn-group-export">
            <button class="btn-saas btn-saas-primary" @click="exportReport" :disabled="exporting">
              <span v-if="exporting" class="spinner-border spinner-border-sm me-2"></span>
              <i v-else class="bi bi-gear-wide-connected me-1"></i>
              <span>{{ exporting ? 'Generating Async Report...' : 'Generate Medical Report' }}</span>
            </button>
            <button class="btn-saas btn-saas-success" @click="downloadReport" :disabled="!canDownload">
              <i class="bi bi-download me-1"></i> Download CSV
            </button>
          </div>

          <div v-if="exportMessage" :class="exportMessage.type === 'text-success' ? 'export-status-box status-ready' : 'export-status-box status-error'">
            <i :class="exportMessage.type === 'text-success' ? 'bi bi-check-circle-fill me-2 text-success' : 'bi bi-exclamation-triangle-fill me-2 text-danger'"></i>
            <span>{{ exportMessage.text }}</span>
          </div>
        </div>
      </div>

    </div>

    <!-- =======================================================================
         TREATMENT & PRESCRIPTION INSPECTION MODAL
         ======================================================================= -->
    <div v-if="selectedTreatment" class="modal-backdrop-custom" @click="selectedTreatment = null">
      <div class="modal-card-custom" @click.stop>
        <div class="modal-card-header">
          <div class="d-flex align-items-center gap-2">
            <i class="bi bi-hospital text-primary fs-5"></i>
            <h4 class="modal-title">Electronic Prescription & Diagnosis</h4>
          </div>
          <button class="modal-close-btn" @click="selectedTreatment = null">✕</button>
        </div>

        <div class="modal-card-body">
          <!-- Doctor Context Header -->
          <div class="treatment-meta-box">
            <div class="d-flex align-items-center gap-3">
              <div class="user-avatar avatar-doctor">{{ getInitials(selectedTreatment.doctor) }}</div>
              <div>
                <h5 class="mb-0 fw-bold">Dr. {{ selectedTreatment.doctor }}</h5>
                <span class="spec-pill">{{ selectedTreatment.specialization }}</span>
              </div>
            </div>
            <div class="text-end">
              <span class="date-badge"><i class="bi bi-calendar3 me-1"></i>{{ selectedTreatment.date }}</span>
              <div class="time-badge"><i class="bi bi-clock me-1"></i>{{ formatTime(selectedTreatment.time) }}</div>
            </div>
          </div>

          <!-- Diagnosis Section -->
          <div class="treatment-section-view">
            <div class="section-badge-view"><i class="bi bi-search-heart me-1"></i> CLINICAL DIAGNOSIS</div>
            <div class="content-box">{{ selectedTreatment.diagnosis }}</div>
          </div>

          <!-- Prescription Section -->
          <div class="treatment-section-view">
            <div class="section-badge-view badge-meds"><i class="bi bi-capsule-pill me-1"></i> PRESCRIPTION & MEDICATION PLAN</div>
            <div class="content-box prescription-box">{{ selectedTreatment.prescription }}</div>
          </div>
        </div>

        <div class="modal-card-footer">
          <button class="btn-saas btn-saas-outline" @click="selectedTreatment = null">Close Record</button>
        </div>
      </div>
    </div>

  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'PatientDashboard',
  data() {
    return {
      patientName: localStorage.getItem('name') || 'Patient',
      patientId: localStorage.getItem('user_id'),
      profile: {},
      doctors: [],
      appointments: [],
      filter: '',
      exporting: false,
      canDownload: false,
      exportMessage: null,
      selectedTreatment: null,
      doctorAvailability: [],
      availabilityDates: [],
      stats: [
        { title: 'Upcoming', value: 0 },
        { title: 'Total Appointments', value: 0 },
        { title: 'Doctors Visited', value: 0 }
      ]
    }
  },
  computed: {
    specializations() {
      return [...new Set(this.doctors.map(d => d.specialization).filter(Boolean))]
    },
    filteredDoctors() {
      return this.filter ? this.doctors.filter(d => d.specialization === this.filter) : this.doctors
    },
    upcomingAppointments() {
      return this.appointments.filter(a => a.status === 'Booked')
    },
    pastAppointments() {
      return this.appointments.filter(a => a.status !== 'Booked')
    }
  },
  async mounted() {
    await this.loadData()
    await this.loadDoctorAvailability()
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
    getDayName(dateStr) {
      const days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
      const date = new Date(dateStr)
      return days[date.getDay()] || ''
    },
    getFormattedDayDate(dateStr) {
      const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
      const date = new Date(dateStr)
      return `${date.getDate()} ${months[date.getMonth()]}`
    },
    formatTime(time) {
      if (!time) return ''
      try {
        const [hours, minutes] = time.split(':')
        const h = parseInt(hours)
        return `${h % 12 || 12}:${minutes} ${h >= 12 ? 'PM' : 'AM'}`
      } catch {
        return time
      }
    },
    async loadDoctorAvailability() {
      try {
        const res = await axios.get('https://nova-life-hospital.onrender.com/api/patient/doctor-availability-week')
        this.availabilityDates = res.data.dates || []
        this.doctorAvailability = res.data.doctors || []
      } catch (error) {
        console.error('Error loading doctor availability:', error)
      }
    },
    async loadData() {
      if (!this.patientId) return
      try {
        const [profileRes, docsRes, apptRes] = await Promise.all([
          axios.get(`https://nova-life-hospital.onrender.com/api/patient/profile/${this.patientId}`),
          axios.get('https://nova-life-hospital.onrender.com/api/doctors'),
          axios.get(`https://nova-life-hospital.onrender.com/api/patient/appointments/${this.patientId}`)
        ])

        this.profile = profileRes.data || {}
        this.doctors = (docsRes.data.data || []).map(doc => ({
          ...doc,
          slots: [],
          selectedSlot: ''
        }))
        this.appointments = apptRes.data.data || []

        this.stats[0].value = this.upcomingAppointments.length
        this.stats[1].value = this.appointments.length
        this.stats[2].value = new Set(this.appointments.map(a => a.doctor)).size
      } catch (error) {
        console.error('Failed to load patient dashboard data:', error)
      }
    },
    async loadSlots(d) {
      if (d.slots.length > 0) return
      try {
        const res = await axios.get(`https://nova-life-hospital.onrender.com/api/patient/available-slots/${d.id}`)
        d.slots = res.data.data || []
      } catch (error) {
        console.error('Error loading slots:', error)
      }
    },
    async book(d) {
      if (!d.selectedSlot) {
        alert('Please select a consultation slot first')
        return
      }
      try {
        await axios.post('https://nova-life-hospital.onrender.com/api/patient/book-appointment', {
          doctor_id: d.id,
          patient_id: this.patientId,
          slot_id: d.selectedSlot.id
        })
        alert('🎉 Appointment booked successfully!')
        d.selectedSlot = ''
        d.slots = []
        await this.loadData()
        await this.loadDoctorAvailability()
      } catch (error) {
        alert(error.response?.data?.error || 'Failed to book appointment')
      }
    },
    async cancelAppointment(id) {
      if (!confirm('Are you sure you want to cancel this appointment?')) return
      try {
        await axios.put('https://nova-life-hospital.onrender.com/api/patient/cancel-appointment', {
          appointment_id: id
        })
        alert('Appointment cancelled.')
        await this.loadData()
        await this.loadDoctorAvailability()
      } catch (error) {
        alert('Failed to cancel appointment')
      }
    },
    async viewTreatment(appointmentId) {
      try {
        const res = await axios.get(`https://nova-life-hospital.onrender.com/api/patient/treatment-details/${appointmentId}`)
        this.selectedTreatment = res.data
      } catch (error) {
        alert('Failed to load treatment details')
      }
    },
    async exportReport() {
      this.exporting = true
      this.exportMessage = null
      try {
        await axios.post('https://nova-life-hospital.onrender.com/api/patient/export-report', {
          patient_id: parseInt(this.patientId)
        })
        this.exportMessage = {
          text: 'Report generation dispatched! Processing in background (ready in 5s)...',
          type: 'text-success'
        }
        setTimeout(() => {
          this.canDownload = true
          this.exportMessage = {
            text: 'Report ready for download! Click "Download CSV" below.',
            type: 'text-success'
          }
        }, 5000)
      } catch (error) {
        this.exportMessage = {
          text: 'Export failed: ' + (error.response?.data?.error || error.message),
          type: 'text-danger'
        }
      } finally {
        this.exporting = false
      }
    },
    async downloadReport() {
      try {
        const res = await axios.get(`https://nova-life-hospital.onrender.com/api/patient/download-report/${this.patientId}`, {
          responseType: 'blob'
        })
        const url = window.URL.createObjectURL(new Blob([res.data]))
        const link = document.createElement('a')
        link.href = url
        link.setAttribute('download', `treatment_report_patient_${this.patientId}.csv`)
        document.body.appendChild(link)
        link.click()
        link.remove()
        window.URL.revokeObjectURL(url)
        this.exportMessage = { text: 'Medical report downloaded successfully!', type: 'text-success' }
      } catch (error) {
        this.exportMessage = {
          text: 'Download failed. Please ensure report is generated first.',
          type: 'text-danger'
        }
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
.patient-page {
  min-height: calc(100vh - 72px);
  background-color: var(--slate-100);
  padding: 36px 28px 60px;
}

.patient-container {
  max-width: 1440px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 26px;
}

/* ==========================================================================
   TOP BANNER
   ========================================================================== */
.patient-top-banner {
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

.banner-user-info {
  display: flex;
  align-items: center;
  gap: 18px;
}

.avatar-patient-lg {
  width: 56px;
  height: 56px;
  border-radius: var(--radius-lg);
  font-size: 20px;
  background: linear-gradient(135deg, #059669, #10b981);
}

.banner-tag {
  font-size: 11px;
  font-weight: 700;
  color: var(--emerald-600);
  letter-spacing: 1px;
}

.banner-title {
  font-size: 26px;
  font-weight: 800;
  color: var(--slate-900);
  margin-bottom: 2px;
}

.banner-subtitle {
  font-size: 13.5px;
  color: var(--slate-500);
  margin-bottom: 0;
}

.banner-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

/* ==========================================================================
   DEMOGRAPHIC SUMMARY CARD
   ========================================================================== */
.info-summary-card {
  background: white;
  border: 1px solid var(--slate-200);
  border-radius: var(--radius-xl);
  padding: 26px 30px;
  box-shadow: var(--shadow-sm);
}

.card-title-group {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 18px;
}

.info-pills-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 14px;
}

.info-box {
  background: var(--slate-50);
  border: 1px solid var(--slate-200);
  border-radius: var(--radius-md);
  padding: 12px 16px;
  display: flex;
  flex-direction: column;
}

.info-box.full-width {
  grid-column: 1 / -1;
}

.info-label {
  font-size: 11.5px;
  font-weight: 600;
  color: var(--slate-500);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 2px;
}

.info-val {
  font-size: 14px;
  font-weight: 700;
  color: var(--slate-800);
}

/* ==========================================================================
   STATS GRID
   ========================================================================== */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 22px;
}

.kpi-card {
  background: white;
  border: 1px solid var(--slate-200);
  border-radius: var(--radius-xl);
  padding: 26px;
  display: flex;
  align-items: center;
  gap: 20px;
  box-shadow: var(--shadow-sm);
  transition: var(--transition-smooth);
}

.kpi-card:hover {
  transform: translateY(-3px);
  box-shadow: var(--shadow-md);
}

.kpi-icon-wrap {
  width: 56px;
  height: 56px;
  border-radius: var(--radius-lg);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 26px;
  flex-shrink: 0;
}

.kpi-upcoming .kpi-icon-wrap { background: var(--primary-50); color: var(--primary-600); }
.kpi-total .kpi-icon-wrap { background: var(--teal-50); color: var(--teal-600); }
.kpi-doctors .kpi-icon-wrap { background: #fef3c7; color: #d97706; }

.kpi-label {
  display: block;
  font-size: 12.5px;
  font-weight: 600;
  color: var(--slate-500);
  text-transform: uppercase;
}

.kpi-value {
  font-size: 32px;
  font-weight: 800;
  color: var(--slate-900);
  line-height: 1.1;
  margin: 4px 0 2px;
}

.kpi-meta {
  font-size: 12px;
  color: var(--slate-400);
  font-weight: 500;
}

/* ==========================================================================
   7-DAY AVAILABILITY MATRIX
   ========================================================================== */
.availability-matrix-wrapper {
  overflow-x: auto;
  border: 1px solid var(--slate-200);
  border-radius: var(--radius-lg);
}

.matrix-table {
  width: 100%;
  border-collapse: collapse;
  min-width: 800px;
}

.matrix-table th {
  background: var(--slate-900);
  color: white;
  padding: 14px 16px;
  font-size: 12px;
  font-weight: 700;
  text-align: center;
  border-right: 1px solid rgba(255, 255, 255, 0.08);
}

.matrix-doctor-th, .matrix-spec-th {
  text-align: left;
}

.matrix-date-header {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.matrix-day {
  font-size: 11px;
  color: #38bdf8;
  text-transform: uppercase;
  letter-spacing: 0.8px;
}

.matrix-cal-date {
  font-size: 13px;
  font-weight: 700;
}

.matrix-table td {
  padding: 14px 16px;
  border-bottom: 1px solid var(--slate-200);
  border-right: 1px solid var(--slate-100);
  vertical-align: middle;
}

.matrix-table tbody tr:hover {
  background: var(--slate-50);
}

.matrix-slot-cell {
  text-align: center;
}

.matrix-chip {
  display: inline-flex;
  align-items: center;
  padding: 4px 10px;
  border-radius: var(--radius-full);
  font-size: 11.5px;
  font-weight: 700;
}

.chip-available {
  background: #d1fae5;
  color: #065f46;
  border: 1px solid #a7f3d0;
}

.chip-unavailable {
  color: var(--slate-300);
  font-weight: 600;
}

/* ==========================================================================
   BOOKING SECTION
   ========================================================================== */
.booking-card {
  background: white;
  border: 1px solid var(--slate-200);
  border-radius: var(--radius-xl);
  padding: 28px 32px;
  box-shadow: var(--shadow-sm);
}

.filter-select {
  min-width: 240px;
}

.doctors-cards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 20px;
  margin-top: 10px;
}

.doctor-booking-card {
  background: var(--slate-50);
  border: 1px solid var(--slate-200);
  border-radius: var(--radius-lg);
  padding: 22px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  transition: var(--transition-smooth);
}

.doctor-booking-card:hover {
  background: white;
  border-color: var(--primary-300);
  box-shadow: var(--shadow-md);
  transform: translateY(-2px);
}

.doc-card-top {
  display: flex;
  align-items: center;
  gap: 14px;
  margin-bottom: 16px;
}

.doc-card-name {
  font-size: 16px;
  font-weight: 700;
  color: var(--slate-900);
  margin-bottom: 4px;
}

/* ==========================================================================
   TABLES
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
  flex-wrap: wrap;
  gap: 12px;
}

.table-header-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.saas-card-title {
  font-size: 18px;
  font-weight: 700;
  color: var(--slate-900);
  margin-bottom: 0;
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
  gap: 10px;
}

.user-avatar-sm {
  width: 34px;
  height: 34px;
  border-radius: var(--radius-full);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 800;
  color: white;
  flex-shrink: 0;
}

.cell-primary-text { font-weight: 600; color: var(--slate-900); }

.spec-pill {
  display: inline-block;
  background: var(--primary-50);
  color: var(--primary-700);
  border: 1px solid var(--primary-200);
  padding: 3px 10px;
  border-radius: var(--radius-full);
  font-size: 12px;
  font-weight: 600;
}

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

.btn-action-view {
  background: var(--slate-100);
  color: var(--slate-800);
  border-color: var(--slate-200);
}

.btn-action-view:hover {
  background: var(--primary-50);
  color: var(--primary-700);
  border-color: var(--primary-200);
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

.table-empty-message {
  text-align: center;
  padding: 30px;
  color: var(--slate-400);
  font-size: 13.5px;
}

/* ==========================================================================
   EXPORT REPORT CARD
   ========================================================================== */
.export-card {
  background: white;
  border: 1px solid var(--slate-200);
  border-radius: var(--radius-xl);
  padding: 28px 32px;
  box-shadow: var(--shadow-sm);
}

.export-icon-circle {
  width: 50px;
  height: 50px;
  border-radius: var(--radius-lg);
  background: linear-gradient(135deg, #059669, #10b981);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  flex-shrink: 0;
}

.saas-card-subtitle {
  font-size: 13.5px;
  color: var(--slate-500);
  margin-bottom: 0;
}

.export-controls-row {
  margin-top: 20px;
  padding-top: 18px;
  border-top: 1px solid var(--slate-100);
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.btn-group-export {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.btn-saas-success {
  background: #10b981;
  color: white;
}

.btn-saas-success:hover:not(:disabled) {
  background: #059669;
  color: white;
}

.export-status-box {
  display: inline-flex;
  align-items: center;
  padding: 10px 16px;
  border-radius: var(--radius-md);
  font-size: 13px;
  font-weight: 600;
  width: fit-content;
}

.status-ready {
  background: #ecfdf5;
  color: #065f46;
  border: 1px solid #a7f3d0;
}

.status-error {
  background: #fef2f2;
  color: #991b1b;
  border: 1px solid #fecaca;
}

/* ==========================================================================
   TREATMENT MODAL
   ========================================================================== */
.modal-backdrop-custom {
  position: fixed;
  inset: 0;
  background: rgba(15, 23, 42, 0.6);
  backdrop-filter: blur(8px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
  padding: 20px;
}

.modal-card-custom {
  background: white;
  border-radius: var(--radius-xl);
  width: 100%;
  max-width: 640px;
  max-height: 85vh;
  display: flex;
  flex-direction: column;
  box-shadow: var(--shadow-xl);
  border: 1px solid var(--slate-200);
  overflow: hidden;
}

.modal-card-header {
  padding: 20px 24px;
  background: var(--slate-50);
  border-bottom: 1px solid var(--slate-200);
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.modal-title {
  font-size: 18px;
  font-weight: 700;
  color: var(--slate-900);
  margin-bottom: 0;
}

.modal-close-btn {
  background: transparent;
  border: none;
  font-size: 18px;
  color: var(--slate-400);
  cursor: pointer;
}

.modal-card-body {
  padding: 24px;
  overflow-y: auto;
}

.treatment-meta-box {
  background: var(--slate-50);
  border: 1px solid var(--slate-200);
  border-radius: var(--radius-md);
  padding: 16px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
}

.treatment-section-view {
  margin-bottom: 20px;
}

.section-badge-view {
  font-size: 11.5px;
  font-weight: 700;
  color: var(--primary-700);
  letter-spacing: 0.8px;
  margin-bottom: 6px;
}

.section-badge-view.badge-meds {
  color: var(--teal-700);
}

.content-box {
  background: var(--slate-50);
  border: 1px solid var(--slate-200);
  border-radius: var(--radius-md);
  padding: 14px 16px;
  font-size: 14px;
  color: var(--slate-800);
  line-height: 1.5;
  white-space: pre-wrap;
}

.modal-card-footer {
  padding: 16px 24px;
  background: var(--slate-50);
  border-top: 1px solid var(--slate-200);
  display: flex;
  justify-content: flex-end;
}

/* ==========================================================================
   RESPONSIVENESS
   ========================================================================== */
@media (max-width: 991px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }

  .patient-top-banner {
    flex-direction: column;
    align-items: flex-start;
  }
}

@media (max-width: 768px) {
  .patient-page {
    padding: 20px 14px;
  }

  .doctors-cards-grid {
    grid-template-columns: 1fr;
  }
}
</style>