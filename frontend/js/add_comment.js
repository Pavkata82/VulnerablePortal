async function addComment(event) {
  event.preventDefault();

  const content = document.getElementById("content").value;
  const message = document.getElementById("message");

  try {
    const response = await fetch(`${API_URL}/comments`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ content }),
    });

    const result = await response.json();

    if (response.ok) {
      message.textContent = result.message;
      message.className =
        "mt-5 rounded-lg bg-green-50 p-3 text-sm text-green-600";

      document.getElementById("register-form").reset();
    } else {
      message.textContent = result.message;
      message.className = "mt-5 rounded-lg bg-red-50 p-3 text-sm text-red-600";
    }
  } catch (error) {
    console.error("Uploading error:", error);

    message.textContent = "Could not connect to the server.";
    message.className = "mt-5 rounded-lg bg-red-50 p-3 text-sm text-red-600";
  }
}
