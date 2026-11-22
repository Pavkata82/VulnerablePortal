async function loadComments() {
  const message = document.getElementById("message");
  const comments = document.getElementById("comments-content");

  try {
    const response = await fetch("/api/comments");
    const result = await response.json();

    if (!response.ok) {
      message.textContent = result.message || "Failed to load comments.";
      message.className = "mt-5 text-sm text-red-600";
      return;
    }

    comments.innerHTML = "";

    result.comments.forEach((comment) => {
      const paragraphUsername = document.createElement("p");
      const paragraphContent = document.createElement("p");

      paragraphUsername.className = "mt-2 text-lg font-semibold text-slate-900";
      paragraphContent.className = "mt-2 text-lg font-semibold text-slate-900";

      paragraphUsername.textContent = comment.username;

      // Intentionally vulnerable to Stored XSS
      paragraphContent.innerHTML = comment.content;

      comments.appendChild(paragraphUsername);
      comments.appendChild(paragraphContent);
    });
  } catch (error) {
    console.error("Comments error:", error);

    message.textContent = "Could not load comments information.";
    message.className = "mt-5 text-sm text-red-600";
  }
}

loadComments();
