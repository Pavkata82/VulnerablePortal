async function searchUsers(event) {
  event.preventDefault();

  const username = document.getElementById("username").value;
  const message = document.getElementById("message");
  const results = document.getElementById("search-results");

  message.textContent = "";
  results.innerHTML = "";

  try {
    const response = await fetch(
      `/api/search?username=${encodeURIComponent(username)}`,
    );

    const result = await response.json();

    if (!response.ok) {
      message.textContent = result.message || "Search failed.";
      message.className = "mt-5 text-sm text-red-600";
      return;
    }

    if (result.users.length === 0) {
      results.textContent = "No users found.";
      results.className = "mt-6 text-sm text-slate-500";
      return;
    }

    result.users.forEach((user) => {
      const userCard = document.createElement("div");

      userCard.className = "mb-3 rounded-xl bg-slate-50 p-5";

      const usernameElement = document.createElement("p");
      usernameElement.className = "text-lg font-semibold text-slate-900";

      const userIdElement = document.createElement("p");
      userIdElement.className = "mt-1 text-sm text-slate-500";

      usernameElement.textContent = user.username;
      userIdElement.textContent = `User ID: ${user.id}`;

      userCard.appendChild(usernameElement);
      userCard.appendChild(userIdElement);

      results.appendChild(userCard);
    });
  } catch (error) {
    console.error("Search error:", error);

    message.textContent = "Could not connect to the server.";
    message.className = "mt-5 text-sm text-red-600";
  }
}
