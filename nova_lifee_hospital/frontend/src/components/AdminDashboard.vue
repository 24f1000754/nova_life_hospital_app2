<template>
  <div class="admin-page">
    <div class="admin-container">
      
      <!-- Top Operational Header -->
      <div class="admin-top-banner">
        <div class="banner-left">
          <div class="banner-badge">
            <i class="bi bi-shield-lock-fill me-1"></i> HOSPITAL ADMINISTRATION CONSOLE
          </div>
          <h1 class="banner-title">Administrative Operations Hub</h1>
          <p class="banner-subtitle">Monitor clinical capacity, manage doctors and patient registries, and supervise appointments.</p>
        </div>
        <div class="banner-right">
          <button class="btn-banner-action" @click="loadAll">
            <i class="bi bi-arrow-clockwise me-1"></i> Refresh Data
          </button>
        </div>
      </div>

      <!-- Global Live Search Bar -->
      <div class="search-card">
        <div class="search-input-wrapper">
          <i class="bi bi-search search-icon"></i>
          <input
            type="text"
            class="search-input"
            placeholder="Search doctors, patients, specializations, or appointments..."
            v-model="search"
            @input="searchAdmin"
          />
          <button v-if="search" class="search-clear-btn" @click="clearSearch" aria-label="Clear search">✕</button>
        </div>
        <div v-if="search" class="search-hint">
          <span>Filtering active records for <strong>"{{ search }}"</strong></span>
        </div>
      </div>

      <!-- KPI Metric Cards Grid -->
      <div class="stats-grid">
        <div class="kpi-card kpi-doctors">
          <div class="kpi-icon-wrap">
            <i class="bi bi-people-fill"></i>
          </div>
          <div class="kpi-body">
            <span class="kpi-label">Active Doctors</span>
            <h2 class="kpi-value">{{ stats.doctors ?? 0 }}</h2>
            <span class="kpi-meta"><i class="bi bi-check2-circle text-success me-1"></i>Specialists & Consultants</span>
          </div>
        </div>

        <div class="kpi-card kpi-patients">
          <div class="kpi-icon-wrap">
            <i class="bi bi-person-lines-fill"></i>
          </div>
          <div class="kpi-body">
            <span class="kpi-label">Registered Patients</span>
            <h2 class="kpi-value">{{ stats.patients ?? 0 }}</h2>
            <span class="kpi-meta"><i class="bi bi-hospital text-info me-1"></i>Enrolled in Records</span>
          </div>
        </div>

        <div class="kpi-card kpi-appointments">
          <div class="kpi-icon-wrap">
            <i class="bi bi-calendar2-check-fill"></i>
          </div>
          <div class="kpi-body">
            <span class="kpi-label">Total Appointments</span>
            <h2 class="kpi-value">{{ stats.appointments ?? 0 }}</h2>
            <span class="kpi-meta"><i class="bi bi-activity text-warning me-1"></i>Consultation Visits</span>
          </div>
        </div>
      </div>

      <!-- Two Column Management Grid (Create Doctor & Doctor Availability) -->
      <div class="management-grid">
        <!-- 1. Add Doctor Card -->
        <div class="saas-card">
          <div class="saas-card-header">
            <div class="card-header-icon header-icon-blue">
              <i class="bi bi-person-plus-fill"></i>
            </div>
            <div>
              <h4 class="saas-card-title">Add Medical Specialist</h4>
              <p class="saas-card-subtitle">Onboard a new physician into the hospital system</p>
            </div>
          </div>

          <form @submit.prevent="createDoctor" class="saas-card-body">
            <div class="row g-3 mb-3">
              <div class="col-md-6">
                <label class="saas-label">Doctor Name <span class="text-danger">*</span></label>
                <div class="input-icon-wrap">
                  <i class="bi bi-person"></i>
                  <input v-model="form.name" required class="saas-form-control" placeholder="Dr. Jane Smith" />
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
              <div class="col-md-6">
                <label class="saas-label">Password <span class="text-danger">*</span></label>
                <div class="input-icon-wrap">
                  <i class="bi bi-lock"></i>
                  <input v-model="form.password" type="password" required class="saas-form-control" placeholder="••••••••" />
                </div>
              </div>

              <div class="col-md-6">
                <label class="saas-label">Specialization <span class="text-danger">*</span></label>
                <div class="input-icon-wrap">
                  <i class="bi bi-tag"></i>
                  <input v-model="form.specialization" required class="saas-form-control" placeholder="Cardiology, Neurology..." />
                </div>
              </div>
            </div>

            <div class="mb-3">
              <label class="saas-label">Professional Bio & Credentials</label>
              <textarea v-model="form.bio" rows="2" class="saas-form-control" placeholder="Brief clinical background, degrees, or awards..."></textarea>
            </div>

            <button type="submit" class="btn-saas-action btn-blue-gradient w-100" :disabled="creatingDoctor">
              <span v-if="creatingDoctor" class="spinner-border spinner-border-sm me-2"></span>
              <i v-else class="bi bi-person-check me-2"></i>
              <span>Create Doctor Profile</span>
            </button>
          </form>
        </div>

        <!-- 2. Add Doctor Availability Slot Card -->
        <div class="saas-card">
          <div class="saas-card-header">
            <div class="card-header-icon header-icon-teal">
              <i class="bi bi-calendar-plus-fill"></i>
            </div>
            <div>
              <h4 class="saas-card-title">Doctor Availability Slots</h4>
              <p class="saas-card-subtitle">Publish consultation slots for appointments</p>
            </div>
          </div>

          <div class="saas-card-body">
            <div class="mb-3">
              <label class="saas-label">Select Doctor <span class="text-danger">*</span></label>
              <select v-model="selectedDoctor" class="saas-form-select">
                <option disabled value="">Choose a doctor from registry...</option>
                <option v-for="d in doctors" :key="d.id" :value="d">
                  Dr. {{ d.name }} — {{ d.specialization || 'General' }}
                </option>
              </select>
            </div>

            <div class="row g-2 mb-3">
              <div class="col-md-5">
                <label class="saas-label">Date</label>
                <input type="date" v-model="slot.date" class="saas-form-control" :min="todayDateStr" />
              </div>
              <div class="col-md-4">
                <label class="saas-label">Time</label>
                <input type="time" v-model="slot.time" class="saas-form-control" />
              </div>
              <div class="col-md-3 d-flex align-items-end">
                <button class="btn-saas-action btn-teal-gradient w-100" @click="addSlot" :disabled="!selectedDoctor || !slot.date || !slot.time">
                  <i class="bi bi-plus-lg me-1"></i> Add
                </button>
              </div>
            </div>

            <!-- Existing Slots List -->
            <div v-if="selectedDoctor" class="slots-container">
              <div class="slots-header">
                <span class="slots-title">Active Slots for Dr. {{ selectedDoctor.name }}</span>
                <span class="slots-count">{{ slots.length }} slots</span>
              </div>

              <div v-if="slots.length" class="slots-chips-grid">
                <div class="slot-chip" v-for="s in slots" :key="s.id" :class="{ 'slot-booked': s.is_booked }">
                  <div class="slot-chip-info">
                    <span class="slot-date">{{ s.date }}</span>
                    <span class="slot-time">{{ formatTime(s.time) }}</span>
                    <span v-if="s.is_booked" class="slot-status-tag">Booked</span>
                  </div>
                  <button class="btn-slot-delete" @click="deleteSlot(s.id)" title="Delete Slot">
                    <i class="bi bi-trash3-fill"></i>
                  </button>
                </div>
              </div>

              <div v-else class="empty-state-slots">
                <i class="bi bi-calendar2-x text-muted"></i>
                <p>No availability slots configured for this doctor yet.</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 3. All Doctors Directory Table -->
      <div class="saas-card table-section-card">
        <div class="table-card-header">
          <div class="table-header-left">
            <h4 class="saas-card-title">Hospital Doctors Registry</h4>
            <span class="badge-counter">{{ doctors.length }} Doctors</span>
          </div>
        </div>

        <div class="saas-table-wrapper">
          <table class="saas-table">
            <thead>
              <tr>
                <th>Doctor Name</th>
                <th>Contact & Email</th>
                <th>Specialization</th>
                <th>Status</th>
                <th class="text-end">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="d in doctors" :key="d.id">
                <td>
                  <div class="user-cell">
                    <div class="user-avatar-sm avatar-doctor">
                      {{ getInitials(d.name) }}
                    </div>
                    <div class="user-cell-meta">
                      <span class="cell-primary-text">Dr. {{ d.name }}</span>
                      <span class="cell-secondary-text">ID #{{ d.id }}</span>
                    </div>
                  </div>
                </td>
                <td>
                  <div class="contact-cell">
                    <span class="cell-primary-text">{{ d.email }}</span>
                    <span v-if="d.address" class="cell-secondary-text"><i class="bi bi-geo-alt me-1"></i>{{ d.address }}</span>
                  </div>
                </td>
                <td>
                  <span class="spec-pill">{{ d.specialization || 'General Practitioner' }}</span>
                </td>
                <td>
                  <span :class="d.is_blacklisted ? 'status-pill pill-danger' : 'status-pill pill-success'">
                    <span class="pulse-dot"></span>
                    {{ d.is_blacklisted ? 'Suspended / Blacklisted' : 'Active Specialist' }}
                  </span>
                </td>
                <td class="text-end">
                  <div class="table-action-btns">
                    <button class="btn-table-action btn-action-view" @click="viewDoctor(d)" title="View Details">
                      <i class="bi bi-eye-fill"></i> View
                    </button>
                    <button class="btn-table-action btn-action-edit" @click="openEditDoctor(d)" title="Edit Doctor">
                      <i class="bi bi-pencil-fill"></i> Edit
                    </button>
                    <button
                      :class="d.is_blacklisted ? 'btn-table-action btn-action-unblock' : 'btn-table-action btn-action-blacklist'"
                      @click="toggleBlacklist(d)"
                      :title="d.is_blacklisted ? 'Unblock Doctor' : 'Blacklist Doctor'"
                    >
                      <i :class="d.is_blacklisted ? 'bi bi-unlock-fill' : 'bi bi-slash-circle-fill'"></i>
                      {{ d.is_blacklisted ? 'Unblock' : 'Block' }}
                    </button>
                    <button class="btn-table-action btn-action-delete" @click="deleteDoctor(d.id)" title="Delete Doctor">
                      <i class="bi bi-trash-fill"></i>
                    </button>
                  </div>
                </td>
              </tr>
              <tr v-if="doctors.length === 0">
                <td colspan="5" class="table-empty-message">No doctor records found matching criteria.</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- 4. Registered Patients Directory Table -->
      <div class="saas-card table-section-card">
        <div class="table-card-header">
          <div class="table-header-left">
            <h4 class="saas-card-title">Registered Patients Directory</h4>
            <span class="badge-counter badge-counter-teal">{{ patients.length }} Patients</span>
          </div>
        </div>

        <div class="saas-table-wrapper">
          <table class="saas-table">
            <thead>
              <tr>
                <th>Patient Name</th>
                <th>Email Address</th>
                <th>Phone Number</th>
                <th>Demographics</th>
                <th class="text-end">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="p in patients" :key="p.id">
                <td>
                  <div class="user-cell">
                    <div class="user-avatar-sm avatar-patient">
                      {{ getInitials(p.name) }}
                    </div>
                    <div class="user-cell-meta">
                      <span class="cell-primary-text">{{ p.name }}</span>
                      <span class="cell-secondary-text">Patient #{{ p.id }}</span>
                    </div>
                  </div>
                </td>
                <td><span class="cell-primary-text">{{ p.email }}</span></td>
                <td>
                  <span v-if="p.phone" class="phone-pill"><i class="bi bi-telephone-fill me-1"></i>{{ p.phone }}</span>
                  <span v-else class="text-muted">N/A</span>
                </td>
                <td>
                  <span class="cell-secondary-text">
                    {{ p.gender || 'Not specified' }} {{ p.age ? `• ${p.age} yrs` : '' }}
                  </span>
                </td>
                <td class="text-end">
                  <div class="table-action-btns">
                    <button class="btn-table-action btn-action-view" @click="viewPatient(p)" title="View Details">
                      <i class="bi bi-eye-fill"></i> View
                    </button>
                    <button class="btn-table-action btn-action-edit" @click="openEditPatient(p)" title="Edit Details">
                      <i class="bi bi-pencil-fill"></i> Edit
                    </button>
                    <button class="btn-table-action btn-action-delete" @click="deletePatient(p.id)" title="Delete Patient">
                      <i class="bi bi-trash-fill"></i>
                    </button>
                  </div>
                </td>
              </tr>
              <tr v-if="patients.length === 0">
                <td colspan="5" class="table-empty-message">No patient records found.</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- 5. All Appointments Audit Table -->
      <div class="saas-card table-section-card">
        <div class="table-card-header">
          <div class="table-header-left">
            <h4 class="saas-card-title">Hospital Consultation Logs</h4>
            <span class="badge-counter badge-counter-indigo">{{ appointments.length }} Total Visits</span>
          </div>

          <!-- Appointment Filter Tabs -->
          <div class="filter-pills-group">
            <button
              :class="appointmentFilter === 'all' ? 'filter-pill filter-pill-active' : 'filter-pill'"
              @click="appointmentFilter = 'all'"
            >
              All Appointments ({{ appointments.length }})
            </button>
            <button
              :class="appointmentFilter === 'upcoming' ? 'filter-pill filter-pill-active' : 'filter-pill'"
              @click="appointmentFilter = 'upcoming'"
            >
              Upcoming
            </button>
            <button
              :class="appointmentFilter === 'past' ? 'filter-pill filter-pill-active' : 'filter-pill'"
              @click="appointmentFilter = 'past'"
            >
              Past / Completed
            </button>
          </div>
        </div>

        <div class="saas-table-wrapper">
          <table class="saas-table">
            <thead>
              <tr>
                <th>Attending Doctor</th>
                <th>Patient</th>
                <th>Appointment Date</th>
                <th>Time Slot</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="a in filteredAppointments" :key="a.id">
                <td>
                  <div class="d-flex align-items-center gap-2">
                    <i class="bi bi-heart-pulse text-primary"></i>
                    <strong class="cell-primary-text">Dr. {{ a.doctor }}</strong>
                  </div>
                </td>
                <td>
                  <div class="d-flex align-items-center gap-2">
                    <i class="bi bi-person text-secondary"></i>
                    <span class="cell-primary-text">{{ a.patient }}</span>
                  </div>
                </td>
                <td>
                  <span class="date-badge"><i class="bi bi-calendar3 me-1"></i>{{ a.date }}</span>
                </td>
                <td>
                  <span class="time-badge"><i class="bi bi-clock me-1"></i>{{ formatTime(a.time) }}</span>
                </td>
                <td>
                  <span
                    :class="{
                      'status-pill pill-success': a.status === 'Completed',
                      'status-pill pill-warning': a.status === 'Booked',
                      'status-pill pill-danger': a.status === 'Cancelled'
                    }"
                  >
                    <span class="pulse-dot"></span>
                    {{ a.status }}
                  </span>
                </td>
              </tr>
              <tr v-if="filteredAppointments.length === 0">
                <td colspan="5" class="table-empty-message">No appointments found matching this filter.</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

    </div>

    <!-- =======================================================================
         MODALS & DRAWERS
         ======================================================================= -->

    <!-- View Doctor Modal -->
    <div v-if="viewingDoctor" class="modal-backdrop-custom" @click="viewingDoctor = null">
      <div class="modal-card-custom" @click.stop>
        <div class="modal-card-header">
          <div class="d-flex align-items-center gap-3">
            <div class="user-avatar avatar-doctor">{{ getInitials(viewingDoctor.name) }}</div>
            <div>
              <h4 class="modal-title">Dr. {{ viewingDoctor.name }}</h4>
              <span class="spec-pill">{{ viewingDoctor.specialization || 'Specialist' }}</span>
            </div>
          </div>
          <button class="modal-close-btn" @click="viewingDoctor = null">✕</button>
        </div>

        <div class="modal-card-body">
          <div class="details-grid">
            <div class="detail-item">
              <span class="detail-label">Email Address</span>
              <span class="detail-value">{{ viewingDoctor.email || 'N/A' }}</span>
            </div>
            <div class="detail-item">
              <span class="detail-label">Gender</span>
              <span class="detail-value">{{ viewingDoctor.gender || 'N/A' }}</span>
            </div>
            <div class="detail-item">
              <span class="detail-label">Qualifications</span>
              <span class="detail-value">{{ viewingDoctor.education || 'N/A' }}</span>
            </div>
            <div class="detail-item">
              <span class="detail-label">Experience</span>
              <span class="detail-value">{{ viewingDoctor.experience || 'N/A' }}</span>
            </div>
            <div class="detail-item full-width">
              <span class="detail-label">Professional Bio</span>
              <div class="detail-box-snippet">{{ viewingDoctor.bio || 'No clinical biography provided.' }}</div>
            </div>
            <div class="detail-item full-width">
              <span class="detail-label">Clinic / Hospital Address</span>
              <span class="detail-value">{{ viewingDoctor.address || 'N/A' }}</span>
            </div>
          </div>
        </div>

        <div class="modal-card-footer">
          <button class="btn-saas btn-saas-outline" @click="viewingDoctor = null">Close Details</button>
        </div>
      </div>
    </div>

    <!-- Edit Doctor Modal -->
    <div v-if="editingDoctor" class="modal-backdrop-custom" @click="editingDoctor = null">
      <div class="modal-card-custom" @click.stop>
        <div class="modal-card-header">
          <h4 class="modal-title"><i class="bi bi-pencil-square me-2"></i>Edit Doctor: Dr. {{ editingDoctor.name }}</h4>
          <button class="modal-close-btn" @click="editingDoctor = null">✕</button>
        </div>

        <div class="modal-card-body">
          <div class="mb-3">
            <label class="saas-label">Specialization</label>
            <input v-model="editForm.specialization" class="saas-form-control" placeholder="Specialization" />
          </div>
          <div class="mb-3">
            <label class="saas-label">Biography</label>
            <textarea v-model="editForm.bio" rows="4" class="saas-form-control" placeholder="Clinical Bio"></textarea>
          </div>
        </div>

        <div class="modal-card-footer">
          <button class="btn-saas btn-saas-outline me-2" @click="editingDoctor = null">Cancel</button>
          <button class="btn-saas btn-saas-primary" @click="updateDoctor">Save Changes</button>
        </div>
      </div>
    </div>

    <!-- View Patient Modal -->
    <div v-if="viewingPatient" class="modal-backdrop-custom" @click="viewingPatient = null">
      <div class="modal-card-custom" @click.stop>
        <div class="modal-card-header">
          <div class="d-flex align-items-center gap-3">
            <div class="user-avatar avatar-patient">{{ getInitials(viewingPatient.name) }}</div>
            <div>
              <h4 class="modal-title">{{ viewingPatient.name }}</h4>
              <span class="text-muted small">Registered Patient</span>
            </div>
          </div>
          <button class="modal-close-btn" @click="viewingPatient = null">✕</button>
        </div>

        <div class="modal-card-body">
          <div class="details-grid">
            <div class="detail-item">
              <span class="detail-label">Email Address</span>
              <span class="detail-value">{{ viewingPatient.email || 'N/A' }}</span>
            </div>
            <div class="detail-item">
              <span class="detail-label">Phone Number</span>
              <span class="detail-value">{{ viewingPatient.phone || 'N/A' }}</span>
            </div>
            <div class="detail-item">
              <span class="detail-label">Age</span>
              <span class="detail-value">{{ viewingPatient.age ? `${viewingPatient.age} years` : 'N/A' }}</span>
            </div>
            <div class="detail-item">
              <span class="detail-label">Gender</span>
              <span class="detail-value">{{ viewingPatient.gender || 'N/A' }}</span>
            </div>
            <div class="detail-item full-width">
              <span class="detail-label">Address</span>
              <span class="detail-value">{{ viewingPatient.address || 'N/A' }}</span>
            </div>
          </div>
        </div>

        <div class="modal-card-footer">
          <button class="btn-saas btn-saas-outline" @click="viewingPatient = null">Close Details</button>
        </div>
      </div>
    </div>

    <!-- Edit Patient Modal -->
    <div v-if="editingPatient" class="modal-backdrop-custom" @click="editingPatient = null">
      <div class="modal-card-custom" @click.stop>
        <div class="modal-card-header">
          <h4 class="modal-title"><i class="bi bi-person-gear me-2"></i>Edit Patient Record</h4>
          <button class="modal-close-btn" @click="editingPatient = null">✕</button>
        </div>

        <div class="modal-card-body">
          <div class="mb-3">
            <label class="saas-label">Full Name</label>
            <input v-model="editPatientForm.name" class="saas-form-control" />
          </div>
          <div class="row g-3 mb-3">
            <div class="col-md-6">
              <label class="saas-label">Age</label>
              <input v-model="editPatientForm.age" type="number" class="saas-form-control" />
            </div>
            <div class="col-md-6">
              <label class="saas-label">Gender</label>
              <input v-model="editPatientForm.gender" class="saas-form-control" />
            </div>
          </div>
          <div class="mb-3">
            <label class="saas-label">Phone</label>
            <input v-model="editPatientForm.phone" class="saas-form-control" />
          </div>
          <div class="mb-3">
            <label class="saas-label">Address</label>
            <input v-model="editPatientForm.address" class="saas-form-control" />
          </div>
        </div>

        <div class="modal-card-footer">
          <button class="btn-saas btn-saas-outline me-2" @click="editingPatient = null">Cancel</button>
          <button class="btn-saas btn-saas-primary" @click="updatePatient">Save Changes</button>
        </div>
      </div>
    </div>

  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'AdminDashboard',
  data() {
    return {
      stats: { doctors: 0, patients: 0, appointments: 0 },
      doctors: [],
      patients: [],
      appointments: [],
      search: '',
      selectedDoctor: '',
      slot: { date: '', time: '' },
      slots: [],
      editingDoctor: null,
      editForm: { specialization: '', bio: '' },
      form: { name: '', email: '', password: '', specialization: '', bio: '' },
      viewingDoctor: null,
      viewingPatient: null,
      editingPatient: null,
      editPatientForm: {},
      appointmentFilter: 'all',
      creatingDoctor: false
    }
  },
  computed: {
    todayDateStr() {
      return new Date().toISOString().split('T')[0]
    },
    filteredAppointments() {
      const today = this.todayDateStr
      if (this.appointmentFilter === 'upcoming') {
        return this.appointments.filter(a => a.date >= today && a.status === 'Booked')
      }
      if (this.appointmentFilter === 'past') {
        return this.appointments.filter(a => a.date < today || a.status !== 'Booked')
      }
      return this.appointments
    }
  },
  watch: {
    selectedDoctor() {
      if (this.selectedDoctor && this.selectedDoctor.id) {
        this.loadSlots()
      } else {
        this.slots = []
      }
    }
  },
  async mounted() {
    await this.loadAll()
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
    clearSearch() {
      this.search = ''
      this.loadAll()
    },
    async loadAll() {
      try {
        const [statsRes, docRes, patRes, appRes] = await Promise.all([
          axios.get('http://127.0.0.1:5000/api/admin/stats'),
          axios.get('http://127.0.0.1:5000/api/admin/doctors'),
          axios.get('http://127.0.0.1:5000/api/admin/patients'),
          axios.get('http://127.0.0.1:5000/api/admin/appointments')
        ])

        this.stats = statsRes.data
        this.doctors = docRes.data.data || []
        this.patients = patRes.data.data || []
        this.appointments = appRes.data.data || []
      } catch (err) {
        console.error('Error loading admin dashboard data:', err)
      }
    },
    async createDoctor() {
      this.creatingDoctor = true
      try {
        await axios.post('http://127.0.0.1:5000/api/admin/create-doctor', this.form)
        alert('Doctor account successfully created!')
        this.form = { name: '', email: '', password: '', specialization: '', bio: '' }
        await this.loadAll()
      } catch (err) {
        alert(err.response?.data?.error || 'Failed to create doctor')
      } finally {
        this.creatingDoctor = false
      }
    },
    async addSlot() {
      if (!this.selectedDoctor || !this.slot.date || !this.slot.time) return
      try {
        await axios.post('http://127.0.0.1:5000/api/admin/add-availability', {
          doctor_id: this.selectedDoctor.id,
          date: this.slot.date,
          time: this.slot.time
        })
        this.slot = { date: '', time: '' }
        await this.loadSlots()
      } catch (err) {
        alert(err.response?.data?.error || 'Failed to add availability slot')
      }
    },
    async loadSlots() {
      if (!this.selectedDoctor) return
      try {
        const res = await axios.get(`http://127.0.0.1:5000/api/admin/doctor-slots/${this.selectedDoctor.id}`)
        this.slots = res.data.data || []
      } catch (err) {
        console.error('Error loading doctor slots:', err)
      }
    },
    async deleteSlot(id) {
      if (!confirm('Remove this availability slot?')) return
      try {
        await axios.delete(`http://127.0.0.1:5000/api/admin/delete-slot/${id}`)
        await this.loadSlots()
      } catch (err) {
        alert('Failed to delete slot')
      }
    },
    viewDoctor(d) {
      this.viewingDoctor = d
    },
    viewPatient(p) {
      this.viewingPatient = p
    },
    openEditDoctor(d) {
      this.editingDoctor = d
      this.editForm = { specialization: d.specialization || '', bio: d.bio || '' }
    },
    openEditPatient(p) {
      this.editingPatient = p
      this.editPatientForm = {
        name: p.name || '',
        age: p.age || '',
        gender: p.gender || '',
        phone: p.phone || '',
        address: p.address || ''
      }
    },
    async updateDoctor() {
      try {
        await axios.put(`http://127.0.0.1:5000/api/admin/update-doctor/${this.editingDoctor.id}`, this.editForm)
        alert('Doctor details updated successfully')
        this.editingDoctor = null
        await this.loadAll()
      } catch (err) {
        alert('Failed to update doctor')
      }
    },
    async updatePatient() {
      try {
        await axios.put(`http://127.0.0.1:5000/api/admin/update-patient/${this.editingPatient.id}`, this.editPatientForm)
        alert('Patient details updated successfully')
        this.editingPatient = null
        await this.loadAll()
      } catch (err) {
        alert('Failed to update patient')
      }
    },
    async toggleBlacklist(d) {
      const actionLabel = d.is_blacklisted ? 'Unblock' : 'Blacklist/Block'
      if (!confirm(`${actionLabel} Dr. ${d.name}?`)) return
      try {
        await axios.put(`http://127.0.0.1:5000/api/admin/blacklist-doctor/${d.id}`, {
          is_blacklisted: !d.is_blacklisted
        })
        await this.loadAll()
      } catch (err) {
        alert('Failed to update doctor status')
      }
    },
    async deleteDoctor(id) {
      if (!confirm('Are you sure you want to permanently delete this doctor?')) return
      try {
        await axios.delete(`http://127.0.0.1:5000/api/admin/delete-doctor/${id}`)
        await this.loadAll()
      } catch (err) {
        alert('Failed to delete doctor')
      }
    },
    async deletePatient(id) {
      if (!confirm('Are you sure you want to permanently delete this patient record?')) return
      try {
        await axios.delete(`http://127.0.0.1:5000/api/admin/delete-patient/${id}`)
        await this.loadAll()
      } catch (err) {
        alert('Failed to delete patient')
      }
    },
    async searchAdmin() {
      if (!this.search.trim()) {
        await this.loadAll()
        return
      }
      try {
        const res = await axios.get(`http://127.0.0.1:5000/api/admin/search?q=${encodeURIComponent(this.search)}`)
        this.doctors = res.data.doctors || []
        this.patients = res.data.patients || []

        const searchLower = this.search.toLowerCase()
        this.appointments = this.appointments.filter(
          a =>
            a.doctor.toLowerCase().includes(searchLower) ||
            a.patient.toLowerCase().includes(searchLower) ||
            a.date.includes(this.search)
        )
      } catch (err) {
        console.error('Search error:', err)
      }
    }
  }
}
</script>

<style scoped>
.admin-page {
  min-height: calc(100vh - 72px);
  background-color: var(--slate-100);
  padding: 36px 28px 60px;
}

.admin-container {
  max-width: 1440px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 28px;
}

/* ==========================================================================
   TOP OPERATIONAL BANNER
   ========================================================================== */
.admin-top-banner {
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
  color: var(--primary-600);
  background: var(--primary-50);
  border: 1px solid var(--primary-200);
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

.banner-subtitle {
  font-size: 14px;
  color: var(--slate-500);
  margin-bottom: 0;
}

.btn-banner-action {
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

.btn-banner-action:hover {
  background: var(--slate-100);
  border-color: var(--slate-400);
  color: var(--slate-900);
}

/* ==========================================================================
   SEARCH CARD
   ========================================================================== */
.search-card {
  background: white;
  border: 1px solid var(--slate-200);
  border-radius: var(--radius-lg);
  padding: 16px 20px;
  box-shadow: var(--shadow-sm);
}

.search-input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.search-icon {
  position: absolute;
  left: 16px;
  font-size: 17px;
  color: var(--slate-400);
}

.search-input {
  width: 100%;
  padding: 12px 42px 12px 46px;
  border: 1px solid var(--slate-200);
  background: var(--slate-50);
  border-radius: var(--radius-md);
  font-size: 14.5px;
  font-family: var(--font-primary);
  color: var(--slate-900);
  outline: none;
  transition: var(--transition-smooth);
}

.search-input:focus {
  border-color: var(--primary-500);
  background: white;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.15);
}

.search-clear-btn {
  position: absolute;
  right: 14px;
  background: transparent;
  border: none;
  color: var(--slate-400);
  font-size: 14px;
  cursor: pointer;
}

.search-hint {
  font-size: 12.5px;
  color: var(--primary-600);
  margin-top: 8px;
}

/* ==========================================================================
   KPI STATS GRID
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
  width: 58px;
  height: 58px;
  border-radius: var(--radius-lg);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 26px;
  flex-shrink: 0;
}

.kpi-doctors .kpi-icon-wrap {
  background: var(--primary-50);
  color: var(--primary-600);
}

.kpi-patients .kpi-icon-wrap {
  background: var(--teal-50);
  color: var(--teal-600);
}

.kpi-appointments .kpi-icon-wrap {
  background: #fef3c7;
  color: #d97706;
}

.kpi-label {
  display: block;
  font-size: 13px;
  font-weight: 600;
  color: var(--slate-500);
  text-transform: uppercase;
  letter-spacing: 0.6px;
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
   MANAGEMENT GRID (2 COLUMNS)
   ========================================================================== */
.management-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
}

.saas-card {
  background: white;
  border: 1px solid var(--slate-200);
  border-radius: var(--radius-xl);
  padding: 30px;
  box-shadow: var(--shadow-sm);
}

.saas-card-header {
  display: flex;
  align-items: center;
  gap: 14px;
  margin-bottom: 22px;
  padding-bottom: 16px;
  border-bottom: 1px solid var(--slate-100);
}

.card-header-icon {
  width: 44px;
  height: 44px;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  flex-shrink: 0;
}

.header-icon-blue { background: var(--primary-50); color: var(--primary-600); }
.header-icon-teal { background: var(--teal-50); color: var(--teal-600); }

.saas-card-title {
  font-size: 18px;
  font-weight: 700;
  color: var(--slate-900);
  margin-bottom: 2px;
}

.saas-card-subtitle {
  font-size: 13px;
  color: var(--slate-400);
  margin-bottom: 0;
}

/* Inputs in Card */
.saas-label {
  display: block;
  font-size: 12.5px;
  font-weight: 600;
  color: var(--slate-700);
  margin-bottom: 5px;
}

.input-icon-wrap {
  position: relative;
  display: flex;
  align-items: center;
}

.input-icon-wrap i {
  position: absolute;
  left: 12px;
  font-size: 15px;
  color: var(--slate-400);
  pointer-events: none;
}

.saas-form-control,
.saas-form-select {
  width: 100%;
  padding: 10px 14px;
  background: var(--slate-50);
  border: 1px solid var(--slate-300);
  border-radius: var(--radius-md);
  font-size: 13.5px;
  font-family: var(--font-primary);
  color: var(--slate-800);
  outline: none;
  transition: var(--transition-smooth);
}

.input-icon-wrap .saas-form-control {
  padding-left: 36px;
}

.saas-form-control:focus,
.saas-form-select:focus {
  border-color: var(--primary-500);
  background: white;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.15);
}

.btn-saas-action {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 11px 18px;
  font-size: 14px;
  font-weight: 600;
  border-radius: var(--radius-md);
  border: none;
  cursor: pointer;
  transition: var(--transition-smooth);
  color: white;
}

.btn-blue-gradient {
  background: linear-gradient(135deg, #0284c7, #2563eb);
}

.btn-blue-gradient:hover:not(:disabled) {
  background: linear-gradient(135deg, #0369a1, #1d4ed8);
  transform: translateY(-1px);
  box-shadow: var(--shadow-md);
}

.btn-teal-gradient {
  background: linear-gradient(135deg, #0d9488, #10b981);
}

.btn-teal-gradient:hover:not(:disabled) {
  background: linear-gradient(135deg, #0f766e, #059669);
  transform: translateY(-1px);
}

/* Slots section in Card */
.slots-container {
  margin-top: 18px;
  padding-top: 16px;
  border-top: 1px solid var(--slate-100);
}

.slots-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.slots-title {
  font-size: 13px;
  font-weight: 700;
  color: var(--slate-700);
}

.slots-count {
  font-size: 11.5px;
  font-weight: 600;
  color: var(--slate-500);
}

.slots-chips-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(170px, 1fr));
  gap: 8px;
  max-height: 160px;
  overflow-y: auto;
  padding-right: 4px;
}

.slot-chip {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 6px 10px;
  background: var(--slate-50);
  border: 1px solid var(--slate-200);
  border-radius: var(--radius-sm);
  font-size: 12px;
}

.slot-chip-info {
  display: flex;
  flex-direction: column;
}

.slot-date { font-weight: 600; color: var(--slate-800); }
.slot-time { font-size: 11px; color: var(--slate-500); }

.slot-status-tag {
  font-size: 9.5px;
  font-weight: 700;
  color: #b45309;
  background: #fef3c7;
  padding: 1px 4px;
  border-radius: 3px;
  width: fit-content;
}

.btn-slot-delete {
  background: transparent;
  border: none;
  color: var(--rose-500);
  cursor: pointer;
  padding: 4px;
}

.btn-slot-delete:hover {
  color: var(--rose-600);
}

.empty-state-slots {
  text-align: center;
  padding: 20px;
  color: var(--slate-400);
  font-size: 13px;
}

/* ==========================================================================
   DATA TABLES
   ========================================================================== */
.table-section-card {
  padding: 26px 30px;
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

.badge-counter {
  font-size: 12px;
  font-weight: 700;
  color: var(--primary-700);
  background: var(--primary-50);
  padding: 4px 10px;
  border-radius: var(--radius-full);
}

.badge-counter-teal {
  color: var(--teal-700);
  background: var(--teal-50);
}

.badge-counter-indigo {
  color: #4338ca;
  background: #e0e7ff;
}

/* Filter pills */
.filter-pills-group {
  display: flex;
  gap: 6px;
  background: var(--slate-100);
  padding: 4px;
  border-radius: var(--radius-md);
}

.filter-pill {
  padding: 6px 14px;
  border: none;
  background: transparent;
  font-size: 12.5px;
  font-weight: 600;
  color: var(--slate-600);
  border-radius: var(--radius-sm);
  cursor: pointer;
  transition: var(--transition-smooth);
}

.filter-pill-active {
  background: white;
  color: var(--primary-600);
  box-shadow: var(--shadow-sm);
  font-weight: 700;
}

/* Table styling */
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

/* Cells */
.user-cell {
  display: flex;
  align-items: center;
  gap: 12px;
}

.user-avatar-sm {
  width: 36px;
  height: 36px;
  border-radius: var(--radius-full);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 13px;
  font-weight: 800;
  color: white;
  flex-shrink: 0;
}

.user-cell-meta {
  display: flex;
  flex-direction: column;
}

.cell-primary-text {
  font-weight: 600;
  color: var(--slate-900);
}

.cell-secondary-text {
  font-size: 12px;
  color: var(--slate-500);
}

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

.phone-pill {
  font-size: 12.5px;
  color: var(--slate-700);
  background: var(--slate-100);
  padding: 3px 8px;
  border-radius: 4px;
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
  padding: 5px 10px;
  font-size: 12px;
  font-weight: 600;
  border-radius: var(--radius-sm);
  border: 1px solid transparent;
  cursor: pointer;
  transition: var(--transition-smooth);
}

.btn-action-view {
  background: var(--slate-100);
  color: var(--slate-700);
  border-color: var(--slate-200);
}

.btn-action-view:hover {
  background: var(--slate-200);
  color: var(--slate-900);
}

.btn-action-edit {
  background: #eff6ff;
  color: var(--primary-600);
  border-color: var(--primary-200);
}

.btn-action-edit:hover {
  background: var(--primary-600);
  color: white;
}

.btn-action-blacklist {
  background: #fff1f2;
  color: #be123c;
  border-color: #fecdd3;
}

.btn-action-blacklist:hover {
  background: #be123c;
  color: white;
}

.btn-action-unblock {
  background: #ecfdf5;
  color: #047857;
  border-color: #a7f3d0;
}

.btn-action-unblock:hover {
  background: #047857;
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

.table-empty-message {
  text-align: center;
  padding: 30px;
  color: var(--slate-400);
  font-size: 14px;
}

/* ==========================================================================
   MODALS
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
  max-width: 580px;
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

.modal-close-btn:hover { color: var(--slate-800); }

.modal-card-body {
  padding: 24px;
  overflow-y: auto;
}

.modal-card-footer {
  padding: 16px 24px;
  background: var(--slate-50);
  border-top: 1px solid var(--slate-200);
  display: flex;
  justify-content: flex-end;
}

.details-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.detail-item {
  display: flex;
  flex-direction: column;
}

.detail-item.full-width {
  grid-column: span 2;
}

.detail-label {
  font-size: 12px;
  font-weight: 600;
  color: var(--slate-500);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 2px;
}

.detail-value {
  font-size: 14px;
  font-weight: 600;
  color: var(--slate-900);
}

.detail-box-snippet {
  background: var(--slate-50);
  border: 1px solid var(--slate-200);
  padding: 12px;
  border-radius: var(--radius-sm);
  font-size: 13.5px;
  color: var(--slate-700);
  line-height: 1.5;
  white-space: pre-wrap;
}

/* ==========================================================================
   RESPONSIVENESS
   ========================================================================== */
@media (max-width: 1024px) {
  .management-grid {
    grid-template-columns: 1fr;
  }

  .stats-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .admin-page {
    padding: 20px 14px;
  }

  .details-grid {
    grid-template-columns: 1fr;
  }

  .detail-item.full-width {
    grid-column: span 1;
  }
}
</style>