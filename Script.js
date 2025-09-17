const chatBox = document.getElementById("chat-box");

async function sendMessage() {
  const inputField = document.getElementById("user-input");
  const userMessage = inputField.value.trim();
  if (!userMessage) return;

  addMessage(userMessage, "user");
  inputField.value = "";

  try {
    const botReply = await getBotResponse(userMessage);
    addMessage(botReply, "bot");
  } catch (error) {
    addMessage("Error getting response from AI.", "bot");
    console.error(error);
  }
}

function addMessage(text, sender) {
  const message = document.createElement("div");
  message.classList.add("message", sender);
  message.innerText = text;
  chatBox.appendChild(message);
  chatBox.scrollTop = chatBox.scrollHeight;
}

// Replace with your real API key and call structure
async function getBotResponse(message) {
  const apiKey = "YOUR_OPENAI_API_KEY"; // Replace with your real key

  const response = await fetch("https://api.openai.com/v1/chat/completions", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${apiKey}`
    },
    body: JSON.stringify({
      model: "gpt-3.5-turbo",
      messages: [{ role: "user", content: message }]
    })
  });

  const data = await response.json();
  return data.choices[0].message.content.trim();
}
