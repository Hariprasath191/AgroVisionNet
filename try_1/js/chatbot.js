function toggleChat() {
  document.getElementById("chatbox").classList.toggle("hidden");
}

function sendMessage() {
  const input = document.getElementById("msg");
  const chat = document.getElementById("messages");

  chat.innerHTML += `<div class="mb-1">You: ${input.value}</div>`;
  chat.innerHTML += `<div class="mb-2 text-green-700">Bot: Use neem oil & improve drainage.</div>`;

  input.value="";
}