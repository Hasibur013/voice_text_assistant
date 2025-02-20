// script.js

let mediaRecorder;
let audioChunks = [];
let isRecording = false;

// Grab DOM elements
const textInput = document.getElementById('text-input');
const sendTextBtn = document.getElementById('send-text');
const openVoicePopupBtn = document.getElementById('open-voice-popup');
const stopRecordingBtn = document.getElementById('stop-recording');
const voicePopup = document.getElementById('voice-popup');
const chatWindow = document.getElementById('chat-window');

// Event listeners
sendTextBtn.addEventListener('click', handleSendText);
openVoicePopupBtn.addEventListener('click', openVoicePopup);
stopRecordingBtn.addEventListener('click', stopRecording);

async function handleSendText() {
  const userText = textInput.value.trim();
  if (!userText) return; // Do nothing if empty

  // Add user's text to the chat interface
  addMessageToChat('user', userText);

  try {
    // POST text to backend
    const response = await fetch('http://localhost:8000/api/text', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text: userText }),
    });
    const data = await response.json();

    // Add the assistant's response (text) to the chat, with optional audio
    addMessageToChat('assistant', data.text_response, data.audio_response);

    // Clear text input
    textInput.value = '';
  } catch (error) {
    console.error('Error sending text:', error);
  }
}

function addMessageToChat(sender, text, audioFilename = null) {
  const messageDiv = document.createElement('div');
  messageDiv.classList.add('message', sender);

  const textPara = document.createElement('p');
  textPara.textContent = text;
  messageDiv.appendChild(textPara);

  // If assistant has an audio file, add a "Listen" button
  if (sender === 'assistant' && audioFilename) {
    const playBtn = document.createElement('button');
    playBtn.textContent = 'Listen';
    playBtn.addEventListener('click', () => {
      const audio = new Audio(`http://localhost:8000/static/audio/${audioFilename}`);
      audio.play();
    });
    messageDiv.appendChild(playBtn);
  }

  chatWindow.appendChild(messageDiv);
  // Scroll to the bottom
  chatWindow.scrollTop = chatWindow.scrollHeight;
}

function openVoicePopup() {
  voicePopup.classList.remove('hidden');
  startRecording();
}

async function startRecording() {
  audioChunks = [];
  try {
    // Ask user for permission to use mic
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder = new MediaRecorder(stream);
    mediaRecorder.start();
    isRecording = true;

    mediaRecorder.addEventListener('dataavailable', event => {
      if (event.data.size > 0) {
        audioChunks.push(event.data);
      }
    });
  } catch (error) {
    console.error('Error accessing microphone:', error);
  }
}

function stopRecording() {
  if (isRecording && mediaRecorder) {
    mediaRecorder.stop();
    isRecording = false;

    mediaRecorder.onstop = async () => {
      // Hide the popup
      voicePopup.classList.add('hidden');
      
      // Create a Blob from recorded chunks
      const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
      audioChunks = [];

      // Show a placeholder in chat for user voice input
      addMessageToChat('user', '[Voice Input]');

      // Upload to /api/voice
      const formData = new FormData();
      formData.append('audio', audioBlob, 'recording.wav');

      try {
        const response = await fetch('http://localhost:8000/api/voice', {
          method: 'POST',
          body: formData,
        });
        const data = await response.json();

        // Show assistant's text response + listen button
        addMessageToChat('assistant', data.text_response, data.audio_response);
      } catch (e) {
        console.error('Error uploading voice:', e);
      }
    };
  }
}
