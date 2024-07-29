let isRecording = false;
const chatBox = document.getElementById('chat-box');
const startRecordingBtn = document.getElementById('start-recording');
const stopRecordingBtn = document.getElementById('stop-recording');

if ('webkitSpeechRecognition' in window && 'speechSynthesis' in window) {
    const recognition = new webkitSpeechRecognition();
    recognition.lang = 'en-US';
    recognition.interimResults = false;
    recognition.continuous = false;

    const requestMicrophoneAccess = async () => {
        try {
            // Request microphone access by attempting to start recognition
            recognition.start();
            recognition.onstart = () => {
                // Microphone access granted
                startRecordingBtn.disabled = true;
                stopRecordingBtn.disabled = false;
            };
            recognition.onerror = (event) => {
                // Handle errors, including permission denial
                if (event.error === 'not-allowed' || event.error === 'not-allowed') {
                    alert('Microphone access was denied. Please allow access in your browser settings.');
                }
            };
        } catch (error) {
            alert('An error occurred while requesting microphone access.');
        }
    };

    requestMicrophoneAccess();

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

            // Play the audio response if available
            if (data.audio_url) {
                const audio = new Audio(data.audio_url);
                audio.play();
            } else {
                // Fallback to browser TTS if audio URL is not provided
                const utterance = new SpeechSynthesisUtterance(assistantMessage);
                const voices = window.speechSynthesis.getVoices();
                utterance.voice = voices.find(voice => voice.name === 'Google US English'); // Choose a more realistic voice
                window.speechSynthesis.speak(utterance);
            }

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
            isRecording = true;
        }
    };

    stopRecordingBtn.onclick = () => {
        if (isRecording) {
            recognition.stop();
            isRecording = false;
        }
    };
} else {
    alert('Speech Recognition or Speech Synthesis API not supported.');
}
