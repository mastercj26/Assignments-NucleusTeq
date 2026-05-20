const API_BASE_URL = "http://localhost:8080";

/**
 * TOKEN STORAGE LOGIC
 * Handled via localStorage for persistence across sessions
 */

function saveUser(token, role, username) {
  localStorage.setItem("token", token);
  localStorage.setItem("role", role);
  localStorage.setItem("username", username);
  localStorage.setItem("loginTime", Date.now()); // For optional session tracking
}

function getToken() {
  return localStorage.getItem("token");
}

function getRole() {
  return localStorage.getItem("role");
}

function getUsername() {
  return localStorage.getItem("username");
}

function logout() {
  localStorage.removeItem("token");
  localStorage.removeItem("role");
  localStorage.removeItem("username");
  localStorage.removeItem("loginTime");
  window.location.href = "login.html";
}

/**
 * ROUTING LOGIC
 * Centralized navigation and access control
 */

function redirectByRole() {
  const role = getRole();
  if (role === "VEHICLE_OWNER" || role === "SUPERADMIN") {
    window.location.href = "admin.html";
  } else if (role === "USER") {
    window.location.href = "dashboard.html";
  } else {
    logout();
  }
}

function requireLogin() {
  if (!getToken()) {
    console.warn("Unauthorized access: No token found. Redirecting to login.");
    window.location.href = "login.html";
    return false;
  }
  return true;
}

function requireVehicleOwner() {
  if (!requireLogin()) return false;
  
  const role = getRole();
  if (role !== "VEHICLE_OWNER" && role !== "SUPERADMIN") {
    console.warn("Access denied: Administrative privileges required.");
    window.location.href = "dashboard.html";
    return false;
  }
  return true;
}

/**
 * API UTILITIES
 * Automatic token attachment and 401/403 handling
 */

async function apiCall(url, method = "GET", body = null) {
  const token = getToken();
  
  const options = {
    method,
    headers: {
      "Content-Type": "application/json"
    }
  };

  if (token) {
    options.headers["Authorization"] = "Bearer " + token;
  }

  if (body) {
    options.body = JSON.stringify(body);
  }

  try {
    const response = await fetch(API_BASE_URL + url, options);

    // If token is expired or invalid, logout and redirect
    if (response.status === 401 || response.status === 403) {
      console.error("Session expired or unauthorized. Logging out...");
      logout();
      return null;
    }

    return response;
  } catch (err) {
    console.error("Network error during API call:", err);
    throw err;
  }
}

async function authRequest(url, body) {
  try {
    const response = await fetch(API_BASE_URL + url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body)
    });

    let data = {};
    try {
      data = await response.json();
    } catch (err) {
      data = {};
    }

    return { response, data };
  } catch (err) {
    console.error("Auth request failed:", err);
    throw err;
  }
}

/**
 * UI UTILITIES
 */

function isValidEmail(email) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

function showMessage(text, type) {
  const box = document.getElementById("message");
  if (!box) return;

  box.textContent = text;
  box.className = "message " + type;
  box.style.display = "block";

  setTimeout(() => {
    box.style.display = "none";
  }, 4000);
}

function showFieldError(fieldId, text) {
  const el = document.getElementById(fieldId);
  if (!el) return;

  el.textContent = text;
  el.style.display = "block";
}

function clearErrors() {
  document.querySelectorAll(".error-text").forEach(el => {
    el.textContent = "";
    el.style.display = "none";
  });

  const msg = document.getElementById("message");
  if (msg) {
    msg.style.display = "none";
  }
}

function setLoading(buttonId, isLoading, text) {
  const btn = document.getElementById(buttonId);
  if (!btn) return;

  btn.disabled = isLoading;
  btn.textContent = text;
  btn.style.opacity = isLoading ? "0.7" : "1";
}

function togglePassword(inputId) {
  const input = document.getElementById(inputId);
  if (!input) return;

  input.type = input.type === "password" ? "text" : "password";
}
