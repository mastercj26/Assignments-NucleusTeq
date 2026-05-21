const API_BASE_URL = "http://localhost:8080";

function saveUser(token, role, username) {

  localStorage.setItem("token", token);

  localStorage.setItem("role", role);

  localStorage.setItem("username", username);

  localStorage.setItem("loginTime", Date.now());
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

  const token = getToken();

  if (!token) {

    window.location.href = "login.html";

    return false;
  }

  return true;
}

function requireVehicleOwner() {

  if (!requireLogin()) {
    return false;
  }

  const role = getRole();

  if (role !== "VEHICLE_OWNER" &&
      role !== "SUPERADMIN") {

    window.location.href = "dashboard.html";

    return false;
  }

  return true;
}

async function apiCall(url, method = "GET", body = null) {

  const token = getToken();

  const options = {
    method: method,
    headers: {
      "Content-Type": "application/json"
    }
  };

  if (token) {

    options.headers["Authorization"] =
        "Bearer " + token;
  }

  if (body) {

    options.body = JSON.stringify(body);
  }

  try {

    const response = await fetch(
        API_BASE_URL + url,
        options
    );

    if (response.status === 401 ||
        response.status === 403) {

      logout();

      return null;
    }

    return response;

  } catch (error) {

    console.log(error);

    throw error;
  }
}

async function authRequest(url, body) {

  try {

    const response = await fetch(
        API_BASE_URL + url,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify(body)
        }
    );

    let data = {};

    try {

      data = await response.json();

    } catch (e) {

      data = {};
    }

    return {
      response,
      data
    };

  } catch (error) {

    console.log(error);

    throw error;
  }
}

function isValidEmail(email) {

  const pattern =
      /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

  return pattern.test(email);
}

function showMessage(text, type) {

  const box =
      document.getElementById("message");

  if (!box) {
    return;
  }

  box.textContent = text;

  box.className = "message " + type;

  box.style.display = "block";

  setTimeout(function () {

    box.style.display = "none";

  }, 4000);
}

function showFieldError(fieldId, text) {

  const element =
      document.getElementById(fieldId);

  if (!element) {
    return;
  }

  element.textContent = text;

  element.style.display = "block";
}

function clearErrors() {

  const errors =
      document.querySelectorAll(".error-text");

  errors.forEach(function (el) {

    el.textContent = "";

    el.style.display = "none";
  });

  const message =
      document.getElementById("message");

  if (message) {

    message.style.display = "none";
  }
}

function setLoading(buttonId, isLoading, text) {

  const button =
      document.getElementById(buttonId);

  if (!button) {
    return;
  }

  button.disabled = isLoading;

  button.textContent = text;

  if (isLoading) {

    button.style.opacity = "0.7";

  } else {

    button.style.opacity = "1";
  }
}

function togglePassword(inputId) {

  const input =
      document.getElementById(inputId);

  if (!input) {
    return;
  }

  if (input.type === "password") {

    input.type = "text";

  } else {

    input.type = "password";
  }
}