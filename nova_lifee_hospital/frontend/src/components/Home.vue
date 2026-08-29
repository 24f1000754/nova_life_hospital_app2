<template>
  <div class="landing-page">
    <!-- Hero Background Mesh & Ambient Glows -->
    <div class="ambient-glow glow-top-left"></div>
    <div class="ambient-glow glow-bottom-right"></div>

    <!-- Main Hero Section -->
    <section class="hero-section">
      <div class="hero-container">
        <!-- Hero Content (Left) -->
        <div class="hero-content">
          <div class="badge-trust">
            <span class="badge-dot"></span>
            <span>NEXT-GEN HEALTHCARE MANAGEMENT PLATFORM</span>
          </div>

          <h1 class="hero-title">
            Intelligent Hospital Care.
            <span class="gradient-text">Human-Centered</span> Medicine.
          </h1>

          <p class="hero-subtitle">
            NovaLife bridges patients, specialists, and clinical operations with real-time appointment scheduling, electronic treatment histories, and comprehensive healthcare workflows.
          </p>

          <!-- Core Stat Counters -->
          <div class="hero-stats-grid">
            <div class="hero-stat-card">
              <div class="stat-icon-wrap stat-icon-cyan">
                <i class="bi bi-clock-history"></i>
              </div>
              <div class="stat-info">
                <h3 class="stat-number">24/7</h3>
                <p class="stat-label">Emergency Care</p>
              </div>
            </div>

            <div class="hero-stat-card">
              <div class="stat-icon-wrap stat-icon-blue">
                <i class="bi bi-people-fill"></i>
              </div>
              <div class="stat-info">
                <h3 class="stat-number">150+</h3>
                <p class="stat-label">Medical Specialists</p>
              </div>
            </div>

            <div class="hero-stat-card">
              <div class="stat-icon-wrap stat-icon-emerald">
                <i class="bi bi-heart-pulse-fill"></i>
              </div>
              <div class="stat-info">
                <h3 class="stat-number">10k+</h3>
                <p class="stat-label">Patients Served</p>
              </div>
            </div>
          </div>

          <!-- Hero Action Buttons -->
          <div class="hero-cta-group">
            <router-link to="/register" class="btn-hero btn-hero-primary">
              <span>Patient Registration</span>
              <i class="bi bi-arrow-right"></i>
            </router-link>

            <router-link to="/login" class="btn-hero btn-hero-secondary">
              <i class="bi bi-shield-lock me-1"></i>
              <span>Portal Login</span>
            </router-link>
          </div>
        </div>

        <!-- Hero Graphic & Feature Card (Right) -->
        <div class="hero-visual">
          <div class="glass-card-main">
            <div class="glass-card-header">
              <div class="pulse-indicator">
                <span class="ping"></span>
                <span class="dot"></span>
              </div>
              <span class="system-status-text">Hospital Operations Active</span>
            </div>

            <h3 class="glass-card-title">Why Choose NovaLife?</h3>
            <p class="glass-card-desc">State-of-the-art clinical infrastructure tailored for prompt recovery and patient satisfaction.</p>

            <div class="features-list">
              <div class="feature-item">
                <div class="feature-icon"><i class="bi bi-cpu"></i></div>
                <div class="feature-text">
                  <strong>Advanced Medical Equipment</strong>
                  <span>High-precision diagnostic imaging and automated lab systems</span>
                </div>
              </div>

              <div class="feature-item">
                <div class="feature-icon"><i class="bi bi-award"></i></div>
                <div class="feature-text">
                  <strong>Board-Certified Doctors</strong>
                  <span>Multidisciplinary specialists available across 12+ clinical domains</span>
                </div>
              </div>

              <div class="feature-item">
                <div class="feature-icon"><i class="bi bi-shield-check"></i></div>
                <div class="feature-text">
                  <strong>Patient-Centered Care</strong>
                  <span>Instant slot booking, electronic prescriptions, and verified reports</span>
                </div>
              </div>

              <div class="feature-item">
                <div class="feature-icon"><i class="bi bi-building-check"></i></div>
                <div class="feature-text">
                  <strong>Modern Infrastructure</strong>
                  <span>Smart inpatient suites, trauma centers, and digital pharmacy</span>
                </div>
              </div>
            </div>

            <div class="emergency-callout">
              <div class="emergency-icon"><i class="bi bi-telephone-inbound-fill"></i></div>
              <div>
                <span class="emergency-label">24/7 Emergency Dispatch Helpline</span>
                <strong class="emergency-phone">1-800-NOVALIFE (668-2543)</strong>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Role Portals Quick Access -->
    <section class="portals-section">
      <div class="portals-container">
        <div class="section-heading">
          <span class="section-tag">ROLE-BASED ACCESS</span>
          <h2 class="section-title">Designed for Every Healthcare Stakeholder</h2>
          <p class="section-desc">Seamlessly navigate to your designated console for personalized medical workflows.</p>
        </div>

        <div class="portals-grid">
          <!-- Patient Portal Card -->
          <div class="portal-card">
            <div class="portal-header portal-header-patient">
              <i class="bi bi-person-heart"></i>
            </div>
            <div class="portal-body">
              <h4>Patient Portal</h4>
              <p>Book appointments with specialists, track 7-day availability, inspect diagnostic treatments, and download medical records.</p>
              <router-link to="/login" class="portal-link">
                <span>Access Patient Portal</span>
                <i class="bi bi-chevron-right"></i>
              </router-link>
            </div>
          </div>

          <!-- Doctor Portal Card -->
          <div class="portal-card">
            <div class="portal-header portal-header-doctor">
              <i class="bi bi-clipboard2-pulse"></i>
            </div>
            <div class="portal-body">
              <h4>Doctor Console</h4>
              <p>Manage daily consultation schedules, publish availability slots, review patient histories, and write electronic prescriptions.</p>
              <router-link to="/login" class="portal-link">
                <span>Doctor Sign In</span>
                <i class="bi bi-chevron-right"></i>
              </router-link>
            </div>
          </div>

          <!-- Admin Portal Card -->
          <div class="portal-card">
            <div class="portal-header portal-header-admin">
              <i class="bi bi-shield-shaded"></i>
            </div>
            <div class="portal-body">
              <h4>Hospital Administration</h4>
              <p>Oversee hospital capacity, onboard specialized doctors, manage patient registries, audit appointments, and monitor metrics.</p>
              <router-link to="/login" class="portal-link">
                <span>Admin Login</span>
                <i class="bi bi-chevron-right"></i>
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
export default {
  name: 'Home'
}
</script>

<style scoped>
.landing-page {
  position: relative;
  background-color: var(--slate-950);
  color: white;
  overflow: hidden;
  min-height: calc(100vh - 72px);
}

/* Ambient glow orbs */
.ambient-glow {
  position: absolute;
  width: 600px;
  height: 600px;
  border-radius: 50%;
  pointer-events: none;
  filter: blur(140px);
  opacity: 0.25;
  z-index: 0;
}

.glow-top-left {
  top: -150px;
  left: -150px;
  background: radial-gradient(circle, #0284c7 0%, rgba(37, 99, 235, 0) 70%);
}

.glow-bottom-right {
  bottom: -150px;
  right: -100px;
  background: radial-gradient(circle, #6366f1 0%, rgba(124, 58, 237, 0) 70%);
}

/* ==========================================================================
   HERO SECTION
   ========================================================================== */
.hero-section {
  position: relative;
  z-index: 1;
  padding: 80px 32px 100px;
}

.hero-container {
  max-width: 1400px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 1.15fr 0.85fr;
  gap: 64px;
  align-items: center;
}

.hero-content {
  display: flex;
  flex-direction: column;
}

.badge-trust {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: rgba(14, 165, 233, 0.12);
  border: 1px solid rgba(14, 165, 233, 0.3);
  padding: 6px 16px;
  border-radius: var(--radius-full);
  font-size: 11.5px;
  font-weight: 700;
  letter-spacing: 1.2px;
  color: #38bdf8;
  width: fit-content;
  margin-bottom: 24px;
}

.badge-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: #38bdf8;
  box-shadow: 0 0 8px #38bdf8;
}

.hero-title {
  font-size: 52px;
  font-weight: 800;
  line-height: 1.15;
  color: white;
  margin-bottom: 20px;
  letter-spacing: -1.2px;
}

.gradient-text {
  background: linear-gradient(135deg, #38bdf8 0%, #818cf8 50%, #c084fc 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.hero-subtitle {
  font-size: 17px;
  line-height: 1.7;
  color: var(--slate-300);
  margin-bottom: 36px;
  max-width: 620px;
}

/* Stats grid */
.hero-stats-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
  margin-bottom: 40px;
}

.hero-stat-card {
  display: flex;
  align-items: center;
  gap: 14px;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.08);
  padding: 16px 18px;
  border-radius: var(--radius-lg);
  backdrop-filter: blur(8px);
  transition: var(--transition-smooth);
}

.hero-stat-card:hover {
  background: rgba(255, 255, 255, 0.07);
  border-color: rgba(56, 189, 248, 0.3);
  transform: translateY(-2px);
}

.stat-icon-wrap {
  width: 44px;
  height: 44px;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
}

.stat-icon-cyan { background: rgba(14, 165, 233, 0.2); color: #38bdf8; }
.stat-icon-blue { background: rgba(99, 102, 241, 0.2); color: #818cf8; }
.stat-icon-emerald { background: rgba(16, 185, 129, 0.2); color: #34d399; }

.stat-number {
  font-size: 24px;
  font-weight: 800;
  color: white;
  line-height: 1.1;
  margin-bottom: 2px;
}

.stat-label {
  font-size: 12px;
  font-weight: 500;
  color: var(--slate-400);
  margin-bottom: 0;
}

/* Hero CTAs */
.hero-cta-group {
  display: flex;
  align-items: center;
  gap: 16px;
  flex-wrap: wrap;
}

.btn-hero {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 14px 28px;
  font-size: 15.5px;
  font-weight: 700;
  border-radius: var(--radius-md);
  text-decoration: none;
  transition: var(--transition-smooth);
}

.btn-hero-primary {
  background: linear-gradient(135deg, #0284c7 0%, #2563eb 100%);
  color: white;
  box-shadow: 0 10px 25px -4px rgba(37, 99, 235, 0.4);
}

.btn-hero-primary:hover {
  background: linear-gradient(135deg, #0369a1 0%, #1d4ed8 100%);
  transform: translateY(-2px);
  box-shadow: 0 14px 30px -4px rgba(37, 99, 235, 0.55);
  color: white;
}

.btn-hero-secondary {
  background: rgba(255, 255, 255, 0.08);
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(6px);
}

.btn-hero-secondary:hover {
  background: rgba(255, 255, 255, 0.15);
  border-color: rgba(255, 255, 255, 0.3);
  color: white;
  transform: translateY(-2px);
}

/* ==========================================================================
   HERO VISUAL (RIGHT GLASS CARD)
   ========================================================================== */
.glass-card-main {
  background: rgba(30, 41, 59, 0.65);
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: var(--radius-xl);
  padding: 36px 32px;
  backdrop-filter: blur(20px);
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5), inset 0 1px 0 0 rgba(255, 255, 255, 0.1);
}

.glass-card-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 16px;
}

.pulse-indicator {
  position: relative;
  width: 10px;
  height: 10px;
}

.pulse-indicator .ping {
  position: absolute;
  width: 100%;
  height: 100%;
  border-radius: 50%;
  background: #10b981;
  opacity: 0.75;
  animation: ping-anim 1.5s cubic-bezier(0, 0, 0.2, 1) infinite;
}

.pulse-indicator .dot {
  position: relative;
  display: inline-block;
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: #10b981;
}

@keyframes ping-anim {
  75%, 100% {
    transform: scale(2.2);
    opacity: 0;
  }
}

.system-status-text {
  font-size: 12px;
  font-weight: 600;
  color: #34d399;
  text-transform: uppercase;
  letter-spacing: 0.8px;
}

.glass-card-title {
  font-size: 24px;
  font-weight: 700;
  color: white;
  margin-bottom: 6px;
}

.glass-card-desc {
  font-size: 13.5px;
  color: var(--slate-300);
  margin-bottom: 24px;
}

.features-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-bottom: 24px;
}

.feature-item {
  display: flex;
  align-items: flex-start;
  gap: 14px;
  padding: 12px 14px;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-radius: var(--radius-md);
  transition: var(--transition-smooth);
}

.feature-item:hover {
  background: rgba(255, 255, 255, 0.06);
  border-color: rgba(56, 189, 248, 0.25);
}

.feature-icon {
  width: 36px;
  height: 36px;
  border-radius: var(--radius-sm);
  background: linear-gradient(135deg, rgba(14, 165, 233, 0.2), rgba(99, 102, 241, 0.2));
  color: #38bdf8;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  flex-shrink: 0;
}

.feature-text {
  display: flex;
  flex-direction: column;
}

.feature-text strong {
  font-size: 14px;
  color: white;
  font-weight: 600;
  margin-bottom: 2px;
}

.feature-text span {
  font-size: 12.5px;
  color: var(--slate-400);
}

.emergency-callout {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 14px 18px;
  background: linear-gradient(135deg, rgba(239, 68, 68, 0.15) 0%, rgba(185, 28, 28, 0.1) 100%);
  border: 1px solid rgba(239, 68, 68, 0.3);
  border-radius: var(--radius-md);
}

.emergency-icon {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: #ef4444;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  flex-shrink: 0;
}

.emergency-label {
  display: block;
  font-size: 11px;
  color: #fca5a5;
  text-transform: uppercase;
  font-weight: 600;
  letter-spacing: 0.5px;
}

.emergency-phone {
  font-size: 15px;
  color: white;
  font-weight: 700;
}

/* ==========================================================================
   ROLE PORTALS SECTION
   ========================================================================== */
.portals-section {
  position: relative;
  z-index: 1;
  background: var(--slate-900);
  border-top: 1px solid rgba(255, 255, 255, 0.08);
  padding: 80px 32px 100px;
}

.portals-container {
  max-width: 1400px;
  margin: 0 auto;
}

.section-heading {
  text-align: center;
  max-width: 650px;
  margin: 0 auto 56px;
}

.section-tag {
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 1.5px;
  color: #38bdf8;
  text-transform: uppercase;
}

.section-title {
  font-size: 36px;
  font-weight: 800;
  color: white;
  margin: 8px 0 12px;
}

.section-desc {
  font-size: 15.5px;
  color: var(--slate-400);
}

.portals-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 28px;
}

.portal-card {
  background: rgba(15, 23, 42, 0.7);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: var(--radius-xl);
  padding: 32px 28px;
  display: flex;
  flex-direction: column;
  transition: var(--transition-smooth);
}

.portal-card:hover {
  background: rgba(30, 41, 59, 0.8);
  border-color: rgba(56, 189, 248, 0.35);
  transform: translateY(-6px);
  box-shadow: 0 20px 35px -5px rgba(0, 0, 0, 0.4);
}

.portal-header {
  width: 54px;
  height: 54px;
  border-radius: var(--radius-lg);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 26px;
  margin-bottom: 22px;
}

.portal-header-patient {
  background: linear-gradient(135deg, rgba(16, 185, 129, 0.2), rgba(5, 150, 105, 0.3));
  color: #34d399;
}

.portal-header-doctor {
  background: linear-gradient(135deg, rgba(14, 165, 233, 0.2), rgba(37, 99, 235, 0.3));
  color: #38bdf8;
}

.portal-header-admin {
  background: linear-gradient(135deg, rgba(99, 102, 241, 0.2), rgba(124, 58, 237, 0.3));
  color: #a78bfa;
}

.portal-body h4 {
  font-size: 20px;
  font-weight: 700;
  color: white;
  margin-bottom: 10px;
}

.portal-body p {
  font-size: 14px;
  color: var(--slate-400);
  line-height: 1.6;
  margin-bottom: 24px;
  min-height: 68px;
}

.portal-link {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-size: 14.5px;
  font-weight: 700;
  color: #38bdf8;
  text-decoration: none;
  transition: var(--transition-smooth);
}

.portal-link:hover {
  color: white;
  transform: translateX(4px);
}

/* ==========================================================================
   RESPONSIVENESS
   ========================================================================== */
@media (max-width: 1100px) {
  .hero-container {
    grid-template-columns: 1fr;
    gap: 48px;
  }

  .hero-title {
    font-size: 42px;
  }

  .portals-grid {
    grid-template-columns: 1fr;
    gap: 20px;
  }

  .portal-body p {
    min-height: auto;
  }
}

@media (max-width: 640px) {
  .hero-title {
    font-size: 32px;
  }

  .hero-stats-grid {
    grid-template-columns: 1fr;
  }

  .hero-cta-group {
    flex-direction: column;
    align-items: stretch;
  }

  .btn-hero {
    justify-content: center;
  }
}
</style>