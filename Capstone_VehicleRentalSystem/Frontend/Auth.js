function saveUser(token, role, username) {
  localStorage.setItem("token",    token);
  localStorage.setItem("role",     role);
  localStorage.setItem("username", username);
}
 
// Get the saved token (returns null if not logged in)
function getToken() {
  return localStorage.getItem("token");
}
 
// Get the saved role (USER or ADMIN)
function getRole() {
  return localStorage.getItem("role");
}
 
// Get the saved username
function getUsername() {
  return localStorage.getItem("username");
}
 
// Remove everything — used when logging out
function logout() {
  localStorage.removeItem("token");
  localStorage.removeItem("role");
  localStorage.removeItem("username");
  window.location.href = "login.html";
}
 
 
// ── 2. ROUTING / PROTECTION ──────────────────────────────────────
// These functions control which page the user can access
 
 
// If logged in, send to the right page based on role
function redirectByRole() {
  const role = getRole();
  if (role === "ADMIN") {
    window.location.href = "admin.html";
  } else {
    window.location.href = "dashboard.html";
  }
}
 
// Call this at top of protected pages (dashboard, admin)
// If user is not logged in, kick them back to login page
function requireLogin() {
  if (!getToken()) {
    window.location.href = "login.html";
  }
}
 
// Call this at top of admin-only pages
// If user is not ADMIN, send them to dashboard
function requireAdmin() {
  requireLogin(); // must be logged in first
  if (getRole() !== "ADMIN") {
    window.location.href = "dashboard.html";
  }
}
 
 
// ── 3. API HELPER ────────────────────────────────────────────────
// This function is used to call any protected API endpoint
// It automatically adds the JWT token to the request header
 
 
async function apiCall(url, method = "GET", body = null) {
  const token = getToken();
 
  // Build the request options
  const options = {
    method: method,
    headers: {
      "Content-Type":  "application/json",
      "Authorization": "Bearer " + token   // attach JWT here
    }
  };
 
  // Add body only for POST, PUT requests
  if (body) {
    options.body = JSON.stringify(body);
  }
 
  const response = await fetch("http://localhost:8080" + url, options);
 
  // If 401 Unauthorized — token expired, send to login
  if (response.status === 401) {
    logout();
    return null;
  }
 
  return response;
}
 
 
// ── 4. VALIDATION HELPERS ────────────────────────────────────────
 
// Check if email looks like a real email
function isValidEmail(email) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}
 
 
// ── 5. UI HELPERS ────────────────────────────────────────────────
// Functions to show messages, errors, and loading state
 
 
// Show a message box (green for success, red for error)
function showMessage(text, type) {
  const box = document.getElementById("message");
  if (!box) return;
 
  box.textContent   = text;
  box.className     = "message " + type; // adds class "success" or "error"
  box.style.display = "block";
 
  // Auto hide after 4 seconds
  setTimeout(() => {
    box.style.display = "none";
  }, 4000);
}
 
// Show red text under a specific input field
function showFieldError(fieldId, text) {
  const el = document.getElementById(fieldId);
  if (el) {
    el.textContent = text;
    el.style.display = "block";
  }
}
 
// Clear all red error texts on the page
function clearErrors() {
  document.querySelectorAll(".error-text").forEach(el => {
    el.textContent = "";
    el.style.display = "none";
  });
  const msg = document.getElementById("message");
  if (msg) msg.style.display = "none";
}
 
// Change button text and disable it while waiting for API
function setLoading(buttonId, isLoading, loadingText) {
  const btn = document.getElementById(buttonId);
  if (!btn) return;
 
  if (isLoading) {
    btn.disabled     = true;
    btn.textContent  = loadingText;
    btn.style.opacity = "0.7";
  } else {
    btn.disabled      = false;
    btn.textContent   = loadingText;
    btn.style.opacity = "1";
  }
}
 
// Show or hide password when eye icon is clicked
function togglePassword(inputId) {
  const input = document.getElementById(inputId);
  if (!input) return;
 
  if (input.type === "password") {
    input.type = "text";
  } else {
    input.type = "password";
  }
}