<template>
  <div id="app" class="app-root">
    <!-- Top Global SaaS Navigation Bar -->
    <header class="saas-navbar">
      <div class="nav-container">
        <!-- Brand Logo & Identity -->
        <router-link to="/" class="nav-brand">
          <div class="brand-icon-wrapper">
            <svg class="brand-pulse-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M3 12H7L10 3L14 21L17 12H21" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </div>
          <div class="brand-text-block">
            <div class="brand-name">Nova<span class="brand-highlight">Life</span></div>
            <div class="brand-tagline">HEALTHCARE SYSTEMS</div>
          </div>
        </router-link>

        <!-- Mobile Menu Toggle Button -->
        <button class="mobile-toggle" @click="mobileMenuOpen = !mobileMenuOpen" aria-label="Toggle navigation">
          <i :class="mobileMenuOpen ? 'bi bi-x-lg' : 'bi bi-list'"></i>
        </button>

        <!-- Navigation Links & User Actions -->
        <nav class="nav-menu" :class="{ 'nav-menu-active': mobileMenuOpen }">
          <!-- Public Links (When not logged in or on landing) -->
          <div class="nav-links-left">
            <router-link to="/" class="nav-link-item" @click="mobileMenuOpen = false">
              <i class="bi bi-house-door me-1"></i> Home
            </router-link>
            
            <template v-if="userRole === 'admin'">
              <router-link to="/admin" class="nav-link-item" @click="mobileMenuOpen = false">
                <i class="bi bi-shield-check me-1"></i> Admin Console
              </router-link>
            </template>

            <template v-else-if="userRole === 'doctor'">
              <router-link to="/doctor" class="nav-link-item" @click="mobileMenuOpen = false">
                <i class="bi bi-heart-pulse me-1"></i> Doctor Portal
              </router-link>
              <router-link to="/doctor/edit-profile" class="nav-link-item" @click="mobileMenuOpen = false">
                <i class="bi bi-person-gear me-1"></i> Edit Profile
              </router-link>
            </template>

            <template v-else-if="userRole === 'patient'">
              <router-link to="/patient" class="nav-link-item" @click="mobileMenuOpen = false">
                <i class="bi bi-hospital me-1"></i> Patient Portal
              </router-link>
              <router-link to="/edit-profile" class="nav-link-item" @click="mobileMenuOpen = false">
                <i class="bi bi-person-circle me-1"></i> Edit Profile
              </router-link>
            </template>
          </div>

          <!-- Auth Actions / Profile Section -->
          <div class="nav-actions">
            <template v-if="!isLoggedIn">
              <router-link to="/login" class="btn-saas btn-saas-outline" @click="mobileMenuOpen = false">
                <i class="bi bi-box-arrow-in-right me-1"></i> Sign In
              </router-link>
              <router-link to="/register" class="btn-saas btn-saas-primary" @click="mobileMenuOpen = false">
                <i class="bi bi-person-plus me-1"></i> Patient Portal
              </router-link>
            </template>

            <template v-else>
              <div class="user-profile-badge">
                <div class="user-avatar" :class="'avatar-' + userRole">
                  {{ userInitials }}
                </div>
                <div class="user-meta">
                  <span class="user-name">{{ userName }}</span>
                  <span class="user-role-pill" :class="'role-pill-' + userRole">
                    <span class="pulse-dot"></span>
                    {{ roleLabel }}
                  </span>
                </div>
              </div>

              <button class="btn-saas btn-saas-danger-soft" @click="handleLogout">
                <i class="bi bi-power me-1"></i> Sign Out
              </button>
            </template>
          </div>
        </nav>
      </div>
    </header>

    <!-- Main Content Area -->
    <main class="main-viewport">
      <router-view />
    </main>

    <!-- Global Healthcare SaaS Footer -->
    <footer class="saas-footer">
      <div class="footer-container">
        <div class="footer-left">
          <div class="footer-brand">Nova<span>Life</span> Hospital</div>
          <p class="footer-desc">Next-generation Clinical Management & Patient Care Infrastructure.</p>
        </div>
        <div class="footer-right">
          <div class="footer-status">
            <span class="status-indicator"></span>
            <span>Healthcare Systems Active & Secure</span>
          </div>
          <p class="footer-copy">© 2026 NovaLife Hospital. Enterprise Hospital Management Platform.</p>
        </div>
      </div>
    </footer>
  </div>
</template>

<script>
export default {
  name: "App",
  data() {
    return {
      mobileMenuOpen: false,
      userName: "",
      userRole: "",
      userId: ""
    }
  },
  computed: {
    isLoggedIn() {
      return !!this.userId && !!this.userRole
    },
    userInitials() {
      if (!this.userName) return "U"
      return this.userName
        .split(" ")
        .map(n => n[0])
        .join("")
        .toUpperCase()
        .slice(0, 2)
    },
    roleLabel() {
      if (this.userRole === "admin") return "Administrator"
      if (this.userRole === "doctor") return "Medical Specialist"
      if (this.userRole === "patient") return "Registered Patient"
      return "User"
    }
  },
  watch: {
    $route() {
      this.syncAuthState()
      this.mobileMenuOpen = false
    }
  },
  mounted() {
    this.syncAuthState()
    window.addEventListener("storage", this.syncAuthState)
  },
  beforeUnmount() {
    window.removeEventListener("storage", this.syncAuthState)
  },
  methods: {
    syncAuthState() {
      this.userName = localStorage.getItem("name") || ""
      this.userRole = localStorage.getItem("role") || ""
      this.userId = localStorage.getItem("user_id") || ""
    },
    handleLogout() {
      localStorage.clear()
      this.syncAuthState()
      this.$router.push("/login")
    }
  }
}
</script>

<style>
/* ==========================================================================
   GLOBAL DESIGN TOKENS & CSS RESET (Healthcare SaaS Design System)
   ========================================================================== */
:root {
  --font-primary: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  --font-heading: 'Outfit', 'Plus Jakarta Sans', sans-serif;

  /* Brand Colors */
  --primary-50: #eff6ff;
  --primary-100: #dbeafe;
  --primary-200: #bfdbfe;
  --primary-500: #3b82f6;
  --primary-600: #2563eb;
  --primary-700: #1d4ed8;

  /* Medical Teal & Emerald */
  --teal-50: #f0fdfa;
  --teal-500: #14b8a6;
  --teal-600: #0d9488;
  --teal-700: #0f766e;
  
  --emerald-500: #10b981;
  --emerald-600: #059669;

  /* Deep Tech Slate Grays */
  --slate-950: #090d16;
  --slate-900: #0f172a;
  --slate-850: #131d36;
  --slate-800: #1e293b;
  --slate-700: #334155;
  --slate-600: #475569;
  --slate-500: #64748b;
  --slate-400: #94a3b8;
  --slate-300: #cbd5e1;
  --slate-200: #e2e8f0;
  --slate-100: #f1f5f9;
  --slate-50: #f8fafc;

  /* Accents */
  --violet-600: #7c3aed;
  --amber-500: #f59e0b;
  --rose-500: #f43f5e;
  --rose-600: #e11d48;

  /* Elevations & Glass */
  --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.07), 0 2px 4px -2px rgba(0, 0, 0, 0.05);
  --shadow-lg: 0 10px 25px -3px rgba(15, 23, 42, 0.08), 0 4px 6px -4px rgba(15, 23, 42, 0.04);
  --shadow-xl: 0 20px 35px -5px rgba(15, 23, 42, 0.12), 0 8px 10px -6px rgba(15, 23, 42, 0.06);
  --shadow-glow: 0 0 25px rgba(37, 99, 235, 0.2);

  --radius-sm: 8px;
  --radius-md: 12px;
  --radius-lg: 16px;
  --radius-xl: 22px;
  --radius-full: 9999px;

  --transition-smooth: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
}

*, *::before, *::after {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

body {
  font-family: var(--font-primary);
  background-color: var(--slate-50);
  color: var(--slate-800);
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  line-height: 1.6;
}

h1, h2, h3, h4, h5, h6 {
  font-family: var(--font-heading);
  color: var(--slate-900);
  letter-spacing: -0.02em;
  font-weight: 700;
}

/* ==========================================================================
   APP CONTAINER & VIEWPORT
   ========================================================================== */
.app-root {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.main-viewport {
  flex: 1;
}

/* ==========================================================================
   GLOBAL NAVBAR
   ========================================================================== */
.saas-navbar {
  position: sticky;
  top: 0;
  z-index: 1000;
  background: rgba(255, 255, 255, 0.94);
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
  border-bottom: 1px solid var(--slate-200);
  box-shadow: var(--shadow-sm);
  transition: var(--transition-smooth);
}

.nav-container {
  max-width: 1440px;
  margin: 0 auto;
  padding: 12px 32px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 24px;
}

/* Brand styling */
.nav-brand {
  display: flex;
  align-items: center;
  gap: 12px;
  text-decoration: none;
  color: inherit;
}

.brand-icon-wrapper {
  width: 44px;
  height: 44px;
  border-radius: var(--radius-md);
  background: linear-gradient(135deg, #0284c7 0%, #2563eb 50%, #4f46e5 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  box-shadow: 0 4px 14px rgba(37, 99, 235, 0.35);
  transition: transform 0.3s ease;
}

.nav-brand:hover .brand-icon-wrapper {
  transform: scale(1.05) rotate(-3deg);
}

.brand-pulse-icon {
  width: 26px;
  height: 26px;
  animation: pulse-beat 2.4s ease-in-out infinite;
}

@keyframes pulse-beat {
  0%, 100% { transform: scale(1); opacity: 0.95; }
  50% { transform: scale(1.1); opacity: 1; }
}

.brand-text-block {
  display: flex;
  flex-direction: column;
}

.brand-name {
  font-family: var(--font-heading);
  font-size: 22px;
  font-weight: 800;
  letter-spacing: -0.5px;
  color: var(--slate-900);
  line-height: 1.1;
}

.brand-highlight {
  background: linear-gradient(135deg, #0284c7, #2563eb);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.brand-tagline {
  font-size: 9.5px;
  font-weight: 700;
  letter-spacing: 1.8px;
  color: var(--slate-400);
}

/* Nav links */
.nav-menu {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex: 1;
  margin-left: 28px;
}

.nav-links-left {
  display: flex;
  align-items: center;
  gap: 8px;
}

.nav-link-item {
  display: inline-flex;
  align-items: center;
  padding: 8px 16px;
  font-size: 14.5px;
  font-weight: 600;
  color: var(--slate-600);
  text-decoration: none;
  border-radius: var(--radius-sm);
  transition: var(--transition-smooth);
}

.nav-link-item:hover {
  color: var(--primary-600);
  background-color: var(--primary-50);
}

.nav-link-item.router-link-active {
  color: var(--primary-600);
  background-color: var(--primary-50);
  font-weight: 700;
}

/* Nav Actions */
.nav-actions {
  display: flex;
  align-items: center;
  gap: 14px;
}

/* User Profile Badge */
.user-profile-badge {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 6px 14px;
  background: var(--slate-100);
  border: 1px solid var(--slate-200);
  border-radius: var(--radius-full);
}

.user-avatar {
  width: 32px;
  height: 32px;
  border-radius: var(--radius-full);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 13px;
  font-weight: 800;
  color: white;
}

.avatar-admin {
  background: linear-gradient(135deg, #4f46e5, #7c3aed);
}

.avatar-doctor {
  background: linear-gradient(135deg, #0284c7, #0d9488);
}

.avatar-patient {
  background: linear-gradient(135deg, #059669, #10b981);
}

.user-meta {
  display: flex;
  flex-direction: column;
}

.user-name {
  font-size: 13.5px;
  font-weight: 700;
  color: var(--slate-800);
  line-height: 1.1;
  max-width: 140px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.user-role-pill {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  font-size: 10.5px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.pulse-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: currentColor;
}

.role-pill-admin { color: #6366f1; }
.role-pill-doctor { color: #0284c7; }
.role-pill-patient { color: #10b981; }

/* Buttons */
.btn-saas {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  padding: 9px 18px;
  font-size: 14px;
  font-weight: 600;
  border-radius: var(--radius-md);
  text-decoration: none;
  cursor: pointer;
  border: 1px solid transparent;
  transition: var(--transition-smooth);
}

.btn-saas-outline {
  background: transparent;
  color: var(--slate-700);
  border-color: var(--slate-300);
}

.btn-saas-outline:hover {
  color: var(--primary-600);
  border-color: var(--primary-500);
  background: var(--primary-50);
}

.btn-saas-primary {
  background: linear-gradient(135deg, #0284c7 0%, #2563eb 100%);
  color: white;
  box-shadow: 0 4px 12px rgba(37, 99, 235, 0.25);
}

.btn-saas-primary:hover {
  background: linear-gradient(135deg, #0369a1 0%, #1d4ed8 100%);
  transform: translateY(-1px);
  box-shadow: 0 6px 16px rgba(37, 99, 235, 0.35);
  color: white;
}

.btn-saas-danger-soft {
  background: #fef2f2;
  color: #dc2626;
  border-color: #fee2e2;
}

.btn-saas-danger-soft:hover {
  background: #fee2e2;
  color: #b91c1c;
}

.mobile-toggle {
  display: none;
  background: transparent;
  border: none;
  font-size: 24px;
  color: var(--slate-700);
  cursor: pointer;
  padding: 4px;
}

/* ==========================================================================
   FOOTER
   ========================================================================== */
.saas-footer {
  background: var(--slate-900);
  color: var(--slate-300);
  border-top: 1px solid var(--slate-800);
  padding: 36px 32px;
  margin-top: auto;
}

.footer-container {
  max-width: 1440px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 20px;
}

.footer-brand {
  font-family: var(--font-heading);
  font-size: 18px;
  font-weight: 700;
  color: white;
}

.footer-brand span {
  color: #38bdf8;
}

.footer-desc {
  font-size: 13px;
  color: var(--slate-400);
  margin-top: 4px;
}

.footer-right {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 6px;
}

.footer-status {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-size: 12.5px;
  font-weight: 600;
  color: #34d399;
}

.status-indicator {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #10b981;
  box-shadow: 0 0 10px #10b981;
}

.footer-copy {
  font-size: 12px;
  color: var(--slate-500);
}

/* ==========================================================================
   RESPONSIVE BREAKPOINTS
   ========================================================================== */
@media (max-width: 991px) {
  .mobile-toggle {
    display: block;
  }

  .nav-menu {
    position: absolute;
    top: 100%;
    left: 0;
    right: 0;
    background: white;
    flex-direction: column;
    align-items: flex-start;
    padding: 20px 28px;
    gap: 20px;
    margin-left: 0;
    border-bottom: 1px solid var(--slate-200);
    box-shadow: var(--shadow-xl);
    display: none;
  }

  .nav-menu-active {
    display: flex;
  }

  .nav-links-left {
    flex-direction: column;
    align-items: flex-start;
    width: 100%;
    gap: 4px;
  }

  .nav-link-item {
    width: 100%;
    padding: 10px 14px;
  }

  .nav-actions {
    flex-direction: column;
    align-items: stretch;
    width: 100%;
    padding-top: 14px;
    border-top: 1px solid var(--slate-100);
  }

  .user-profile-badge {
    justify-content: flex-start;
  }

  .footer-container {
    flex-direction: column;
    align-items: flex-start;
  }

  .footer-right {
    align-items: flex-start;
  }
}
</style>