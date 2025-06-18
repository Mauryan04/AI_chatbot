const chatWindow = document.getElementById("chat-window");
const userInput = document.getElementById("user-input");

function appendMessage(message, sender) {
  const div = document.createElement("div");
  div.className = `chat-bubble ${sender}`;
  div.innerText = message;
  chatWindow.appendChild(div);
  chatWindow.scrollTop = chatWindow.scrollHeight;
}

function sendMessage() {
  const message = userInput.value.trim();
  if (!message) return;

  appendMessage(message, "user");
  userInput.value = "";

  appendMessage("Typing...", "bot");

  fetch("https://0ff9-2409-40f0-501b-7d0-c59d-78a9-1239-5f9f.ngrok-free.app", { // 👈 Replace with hosted backend if needed
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query: message })
  })
  .then(res => res.json())
  .then(data => {
    // Remove "Typing..." placeholder
    const bubbles = document.querySelectorAll(".bot");
    if (bubbles[bubbles.length - 1].innerText === "Typing...") {
      chatWindow.removeChild(bubbles[bubbles.length - 1]);
    }
    appendMessage(data.answer || "Sorry, I don't have that information.", "bot");
  })
  .catch(err => {
    appendMessage("Error fetching response.", "bot");
    console.error(err);
  });
}
