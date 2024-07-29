let isRecording = false;
const chatBox = document.getElementById('chat-box');
const startRecordingBtn = document.getElementById('start-recording');
const stopRecordingBtn = document.getElementById('stop-recording');

// Check if the browser supports Web Speech API
const hasSpeechRecognition = 'webkitSpeechRecognition' in window;
const hasSpeechSynthesis = 'speechSynthesis' in window;

if (hasSpeechRecognition && hasSpeechSynthesis) {
    const recognition = new webkitSpeechRecognition();
    recognition.lang = 'en-US';
    recognition.interimResults = false;

    recognition.onstart = () => {
        isRecording = true;
        startRecordingBtn.disabled = true;
        stopRecordingBtn.disabled = false;
    };

    recognition.onresult = async (event) => {
        const userMessage = event.results[0][0].transcript;
        chatBox.innerHTML += `<div class="message user">${userMessage}</div>`;
        
        try {
            const response = await fetch('http://127.0.0.1:5000/send_message', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: userMessage }),
            });
            const data = await response.json();

            let assistantMessage = data.response || data.error || 'Error: Unknown error';
            chatBox.innerHTML += `<div class="message assistant">${assistantMessage}</div>`;
            
            const utterance = new SpeechSynthesisUtterance(assistantMessage);
            speechSynthesis.speak(utterance);
        } catch (error) {
            chatBox.innerHTML += `<div class="message assistant">Error: ${error.message}</div>`;
        }
    };

    recognition.onerror = (event) => {
        chatBox.innerHTML += `<div class="message assistant">Error: ${event.error}</div>`;
    };

    recognition.onend = () => {
        isRecording = false;
        startRecordingBtn.disabled = false;
        stopRecordingBtn.disabled = true;
    };

    startRecordingBtn.onclick = () => {
        if (!isRecording) {
            recognition.start();
        }
    };

    stopRecordingBtn.onclick = () => {
        if (isRecording) {
            recognition.stop();
        }
    };
} else {
    alert('Speech Recognition or Speech Synthesis API not supported.');
}
