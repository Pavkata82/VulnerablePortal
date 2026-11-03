const API_URL = "http://127.0.0.1:5000/api";

async function addComment(event) {
  event.preventDefault();

  const username = document.getElementById("username").value;
  const content = document.getElementById("content").value;

  try {
    const response = await fetch(`${API_URL}/comments`, {
      method: "POST",

      headers: {
        "Content-Type": "application/json",
      },

      body: JSON.stringify({
        username: username,
        content: content,
      }),
    });

    const result = await response.json();

    const message = document.getElementById("message");

    if (response.ok) {
      message.textContent = result.message;
      message.className =
        "mt-5 text-sm rounded-lg bg-green-50 p-3 text-green-600";

      document.getElementById("register-form").reset();
    } else {
      message.textContent = result.message;
      message.className = "mt-5 text-sm rounded-lg bg-red-50 p-3 text-red-600";
    }
  } catch (error) {
    console.error("Uploading error: ", error);

    const message = document.getElementById("message");

    message.textContent = "Could not connect to the server.";
    message.className = "mt-5 text-sm rounded-lg bg-red-50 p-3 text-red-600";
  }
}
