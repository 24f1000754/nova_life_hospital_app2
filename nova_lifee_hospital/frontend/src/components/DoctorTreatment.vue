<template>
  <div class="treatment-page">
    <div class="treatment-container">
      
      <!-- Top Action Navigation Bar -->
      <div class="treatment-header-card">
        <div class="d-flex align-items-center gap-3">
          <button class="btn-back" @click="$router.push('/doctor')" title="Return to Doctor Console">
            <i class="bi bi-arrow-left"></i>
          </button>
          <div>
            <div class="treatment-tag">ELECTRONIC MEDICAL RECORD</div>
            <h2 class="treatment-title">Clinical Treatment & Prescription Entry</h2>
            <p class="treatment-subtitle">Recording clinical diagnosis, treatment plan, and medications for Appointment #{{ id }}</p>
          </div>
        </div>
      </div>

      <!-- Treatment Editor Card -->
      <div class="saas-card treatment-form-card">
        <form @submit.prevent="saveTreatment">

          <!-- Section 1: Diagnosis -->
          <div class="treatment-section">
            <div class="section-label-group">
              <div class="section-icon icon-diagnosis">
                <i class="bi bi-search-heart"></i>
              </div>
              <div>
                <label class="section-title">1. Clinical Diagnosis & Findings <span class="text-danger">*</span></label>
                <p class="section-hint">Primary diagnosis, presenting symptoms, vital signs, or clinical impressions.</p>
              </div>
            </div>
            <textarea
              v-model="form.diagnosis"
              required
              rows="3"
              class="saas-textarea-clinical"
              placeholder="e.g. Acute bacterial pharyngitis, mild dehydration. Vitals: BP 120/80, Temp 100.4°F..."
            ></textarea>
          </div>

          <!-- Section 2: Treatment Plan -->
          <div class="treatment-section">
            <div class="section-label-group">
              <div class="section-icon icon-treatment">
                <i class="bi bi-bandaid-fill"></i>
              </div>
              <div>
                <label class="section-title">2. Treatment Plan & Clinical Interventions <span class="text-danger">*</span></label>
                <p class="section-hint">Therapeutic course, in-clinic procedures, rest recommendations, or dietary advice.</p>
              </div>
            </div>
            <textarea
              v-model="form.treatment"
              required
              rows="3"
              class="saas-textarea-clinical"
              placeholder="e.g. Prescribed 5-day antibiotic course, warm saline gargles, increased oral hydration..."
            ></textarea>
          </div>

          <!-- Section 3: Prescribed Medications -->
          <div class="treatment-section">
            <div class="section-label-group">
              <div class="section-icon icon-medicines">
                <i class="bi bi-capsule-pill"></i>
              </div>
              <div>
                <label class="section-title">3. Medications, Dosage & Frequency <span class="text-danger">*</span></label>
                <p class="section-hint">List drugs, dosage units (mg), frequency (e.g. 1-0-1 after meals), and duration.</p>
              </div>
            </div>
            <textarea
              v-model="form.medicines"
              required
              rows="3"
              class="saas-textarea-clinical"
              placeholder="e.g. Amoxicillin 500mg (1-0-1 for 5 days), Paracetamol 650mg SOS for fever..."
            ></textarea>
          </div>

          <!-- Section 4: Precautions & Follow-up Suggestions -->
          <div class="treatment-section">
            <div class="section-label-group">
              <div class="section-icon icon-suggestions">
                <i class="bi bi-chat-heart"></i>
              </div>
              <div>
                <label class="section-title">4. Precautions & Follow-up Instructions</label>
                <p class="section-hint">Warning signs requiring emergency attention, diet precautions, or revisit date.</p>
              </div>
            </div>
            <textarea
              v-model="form.suggestions"
              rows="2"
              class="saas-textarea-clinical"
              placeholder="e.g. Avoid cold beverages. Follow-up after 5 days if fever persists..."
            ></textarea>
          </div>

          <!-- Action Buttons -->
          <div class="treatment-form-footer">
            <button type="button" class="btn-saas btn-saas-outline me-3" @click="$router.push('/doctor')">
              Cancel & Discard
            </button>
            <button type="submit" class="btn-saas btn-saas-primary btn-save-treatment" :disabled="saving">
              <span v-if="saving" class="spinner-border spinner-border-sm me-2" role="status"></span>
              <i v-else class="bi bi-check-circle-fill me-2"></i>
              <span>Save & Finalize Treatment</span>
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
  name: 'DoctorTreatment',
  data() {
    return {
      id: this.$route.params.id,
      form: {
        diagnosis: '',
        treatment: '',
        medicines: '',
        suggestions: ''
      },
      saving: false
    }
  },
  methods: {
    async saveTreatment() {
      this.saving = true
      try {
        await axios.put('http://127.0.0.1:5000/api/doctor/add-treatment', {
          appointment_id: this.id,
          diagnosis: this.form.diagnosis,
          prescription:
            this.form.treatment + ' | ' +
            this.form.medicines + ' | ' +
            this.form.suggestions
        })
        alert('✅ Treatment and prescription saved successfully!')
        this.$router.push('/doctor')
      } catch (err) {
        alert(err.response?.data?.error || 'Failed to save treatment')
      } finally {
        this.saving = false
      }
    }
  }
}
</script>

<style scoped>
.treatment-page {
  min-height: calc(100vh - 72px);
  background-color: var(--slate-100);
  padding: 36px 24px 60px;
}

.treatment-container {
  max-width: 900px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

/* Header Card */
.treatment-header-card {
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

.treatment-tag {
  font-size: 11px;
  font-weight: 700;
  color: var(--primary-600);
  letter-spacing: 1px;
}

.treatment-title {
  font-size: 22px;
  font-weight: 800;
  color: var(--slate-900);
  margin: 2px 0;
}

.treatment-subtitle {
  font-size: 13.5px;
  color: var(--slate-500);
  margin-bottom: 0;
}

/* Form Card */
.treatment-form-card {
  background: white;
  border: 1px solid var(--slate-200);
  border-radius: var(--radius-xl);
  padding: 36px 40px;
  box-shadow: var(--shadow-sm);
}

.treatment-section {
  margin-bottom: 28px;
  padding-bottom: 24px;
  border-bottom: 1px solid var(--slate-100);
}

.treatment-section:last-of-type {
  border-bottom: none;
  margin-bottom: 20px;
}

.section-label-group {
  display: flex;
  align-items: flex-start;
  gap: 14px;
  margin-bottom: 12px;
}

.section-icon {
  width: 36px;
  height: 36px;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 17px;
  flex-shrink: 0;
}

.icon-diagnosis { background: var(--primary-50); color: var(--primary-600); }
.icon-treatment { background: var(--teal-50); color: var(--teal-600); }
.icon-medicines { background: #fef3c7; color: #d97706; }
.icon-suggestions { background: #e0e7ff; color: #4f46e5; }

.section-title {
  display: block;
  font-size: 15px;
  font-weight: 700;
  color: var(--slate-900);
  margin-bottom: 2px;
}

.section-hint {
  font-size: 12.5px;
  color: var(--slate-500);
  margin-bottom: 0;
}

.saas-textarea-clinical {
  width: 100%;
  padding: 12px 16px;
  background: var(--slate-50);
  border: 1px solid var(--slate-300);
  border-radius: var(--radius-md);
  font-size: 14px;
  font-family: var(--font-primary);
  color: var(--slate-800);
  line-height: 1.5;
  outline: none;
  resize: vertical;
  transition: var(--transition-smooth);
}

.saas-textarea-clinical:focus {
  border-color: var(--primary-500);
  background: white;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.15);
}

.saas-textarea-clinical::placeholder {
  color: var(--slate-400);
}

.treatment-form-footer {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  padding-top: 10px;
}

.btn-save-treatment {
  padding: 12px 28px;
  font-size: 15px;
}

@media (max-width: 768px) {
  .treatment-form-card {
    padding: 24px 20px;
  }
}
</style>
