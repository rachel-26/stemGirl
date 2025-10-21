console.log("chatAgent.js loaded!");

// DOM elements
const chatBox = document.getElementById("chat-container");
const inputField = document.querySelector("footer input");
const sendBtn = document.querySelector("footer button");

// Load user interest (optional)
const userInterest = localStorage.getItem("userInterest") || "STEM";

// Append message to chat
function appendMessage(sender, text) {
  const wrapper = document.createElement("div");
  wrapper.classList.add("flex", "items-start", "gap-4", "max-w-xl");
  if (sender === "user") wrapper.classList.add("self-end", "flex-row-reverse");

  const avatar = document.createElement("div");
  avatar.className =
    sender === "user"
      ? "w-10 h-10 rounded-full bg-gray-300 dark:bg-gray-600 flex-shrink-0 flex items-center justify-center"
      : "w-10 h-10 rounded-full bg-primary/20 dark:bg-primary/30 flex-shrink-0 flex items-center justify-center";

  const messageContainer = document.createElement("div");
  messageContainer.className =
    sender === "user"
      ? "bg-gray-200 dark:bg-gray-700 p-4 rounded-lg rounded-tr-none max-w-md text-gray-800 dark:text-gray-200"
      : "bg-gradient-to-br from-primary/80 to-primary/60 text-white p-4 rounded-lg rounded-tl-none max-w-md";

  messageContainer.textContent = text;

  wrapper.appendChild(avatar);
  wrapper.appendChild(messageContainer);
  chatBox.appendChild(wrapper);
  chatBox.scrollTop = chatBox.scrollHeight;
}

// Typing indicator
function showTyping() {
  const typingDiv = document.createElement("div");
  typingDiv.className =
    "bg-gradient-to-br from-primary/80 to-primary/60 text-white p-4 rounded-lg rounded-tl-none max-w-md flex space-x-1";
  typingDiv.innerHTML = `
    <div class="w-2 h-2 bg-white rounded-full animate-bounce" style="animation-delay: -0.3s;"></div>
    <div class="w-2 h-2 bg-white rounded-full animate-bounce" style="animation-delay: -0.15s;"></div>
    <div class="w-2 h-2 bg-white rounded-full animate-bounce"></div>
  `;
  chatBox.appendChild(typingDiv);
  chatBox.scrollTop = chatBox.scrollHeight;
  return typingDiv;
}

// Initial greeting
function greetUser() {
  appendMessage(
    "bot",
    `👋 Hi there! I’ve already prepared some ${userInterest} content for you. Feel free to chat or ask me anything.`
  );
}

// Send message to backend
async function sendMessage() {
  const message = inputField.value.trim();
  if (!message) return;

  appendMessage("user", message);
  inputField.value = "";
  inputField.disabled = true;
  sendBtn.disabled = true;

  const typingDiv = showTyping();

  try {
    const response = await fetch("http://127.0.0.1:8000/chatAgent", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message }),
    });

    const data = await response.json();
    chatBox.removeChild(typingDiv);

    appendMessage("bot", data.response || "Sorry, I didn't understand that.");
  } catch (err) {
    console.error("Chat API error:", err);
    chatBox.removeChild(typingDiv);
    appendMessage("bot", "⚠️ I couldn't reach the server. Please try again.");
  } finally {
    inputField.disabled = false;
    sendBtn.disabled = false;
    inputField.focus();
  }
}

// Event listeners
sendBtn.addEventListener("click", sendMessage);
inputField.addEventListener("keypress", (e) => {
  if (e.key === "Enter") sendMessage();
});

// Initialize
window.addEventListener("load", greetUser);
