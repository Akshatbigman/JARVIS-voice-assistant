const AI71_BASE_URL = "https://api.ai71.ai/v1/";
const AI71_API_KEY = "ai71-api-698349c2-ec60-4009-be4d-aaa05ac8a97c";

async function fetchChatCompletion(userMessage) {
  try {
    const response = await fetch(`${AI71_BASE_URL}chat/completions`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${AI71_API_KEY}`
      },
      body: JSON.stringify({
        model: "tiiuae/falcon-180b-chat",
        messages: [
          { role: "system", content: "You are a helpful assistant." },
          { role: "user", content: userMessage }
        ]
      })
    });

    const data = await response.json();
    addMessage('ai', data.choices[0].message.content);
    speakResponse(data.choices[0].message.content);
  } catch (error) {
    console.error('Error fetching chat completion:', error);
    addMessage('error', 'Error fetching response from AI71.');
  }
}

function speakResponse(text) {
  const utterance = new SpeechSynthesisUtterance(text);
  utterance.onerror = (event) => {
    console.error('Speech synthesis error:', event.error);
  };
  window.speechSynthesis.speak(utterance);
}

function addMessage(role, message) {
  const responseContainer = document.getElementById('response');
  const messageElement = document.createElement('div');
  messageElement.className = `message ${role}`;
  messageElement.textContent = message;
  responseContainer.appendChild(messageElement);
  responseContainer.scrollTop = responseContainer.scrollHeight;
}

document.getElementById('start-btn').addEventListener('click', () => {
  const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();

  recognition.continuous = false; // Process only one result at a time
  recognition.interimResults = false; // No need for intermediate results

  recognition.onresult = (event) => {
    const userMessage = event.results[0][0].transcript.trim();
    addMessage('user', userMessage);
    fetchChatCompletion(userMessage);
  };

  recognition.onerror = (event) => {
    console.error('Speech recognition error:', event.error);
    addMessage('error', 'Error recognizing speech.');
  };

  recognition.start();
});
