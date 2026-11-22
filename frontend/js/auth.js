const API_URL = "http://127.0.0.1:5000/api";

async function registerUser(event) {
  event.preventDefault();

  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;

  try {
    const response = await fetch(`${API_URL}/register`, {
      method: "POST",

      headers: {
        "Content-Type": "application/json",
      },

      body: JSON.stringify({
        username: username,
        password: password,
      }),
    });

    const result = await response.json();

    const message = document.getElementById("message");

    if (response.ok) {
      message.textContent = result.message;
      message.className =
        "mb-5 text-sm rounded-lg bg-green-50 p-3 text-green-600";

      document.getElementById("register-form").reset();

      setTimeout(() => {
        window.location.href = "/login";
      }, 3000);
    } else {
      message.textContent = result.message;
      message.className = "mb-5 text-sm rounded-lg bg-red-50 p-3 text-red-600";
    }
  } catch (error) {
    console.error("Registration error:", error);

    const message = document.getElementById("message");

    message.textContent = "Could not connect to the server.";
    message.className = "mb-5 text-sm rounded-lg bg-red-50 p-3 text-red-600";
  }
}

async function loginUser(event) {
  event.preventDefault();

  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;

  const message = document.getElementById("message");

  try {
    const response = await fetch(`${API_URL}/login`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ username, password }),
    });

    const result = await response.json();

    if (response.ok) {
      window.location.href = `/dashboard?user=${encodeURIComponent(result.user.username)}`;
    } else {
      message.textContent = result.message;
      message.className = "mb-5 text-sm rounded-lg bg-red-50 p-3 text-red-600";
    }
  } catch (error) {
    console.error("Login error:", error);

    message.textContent = "Could not connect to the server.";
    message.className = "mb-5 text-sm rounded-lg bg-red-50 p-3 text-red-600";
  }
}

async function logoutUser() {
  try {
    const response = await fetch(`${API_URL}/logout`, {
      method: "POST",
    });

    if (response.ok) {
      window.location.href = "/login";
    }
  } catch (error) {
    console.error("Logout error:", error);
  }
}
