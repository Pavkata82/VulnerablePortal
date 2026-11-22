async function loadDashboard() {
  const message = document.getElementById("message");

  // Get username from URL query parameter
  const urlParams = new URLSearchParams(window.location.search);
  const username = urlParams.get("user");

  if (!username) {
    message.textContent = "No username specified.";
    message.className = "mt-5 text-sm text-red-600";
    return;
  }

  try {
    const response = await fetch(
      `/api/user?username=${encodeURIComponent(username)}`,
    );

    const result = await response.json();

    if (!response.ok) {
      message.textContent = result.message;
      message.className = "mt-5 text-sm text-red-600";
      return;
    }

    // Display user information
    document.getElementById("username").textContent = result.user.username;
    document.getElementById("user-id").textContent = result.user.id;
    document.getElementById("user-name").textContent = result.user.username;
  } catch (error) {
    console.error("Dashboard error:", error);

    message.textContent = "Could not load user information.";
    message.className = "mt-5 text-sm text-red-600";
  }
}

loadDashboard();
