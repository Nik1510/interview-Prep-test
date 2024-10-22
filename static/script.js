let mediaRecorder;
let audioChunks = [];

// Function to fetch a question based on the selected domain
async function fetchQuestion() {
    const domain = document.getElementById('domain').value;
    const questionElement = document.getElementById('question');

    questionElement.innerText = "Fetching question...";
    try {
        const response = await fetch(`/get-question/${domain}`);
        const result = await response.json();

        if (response.ok) {
            questionElement.innerText = result.question;
        } else {
            questionElement.innerText = `Error: ${result.error || "Failed to fetch question."}`;
        }
    } catch (error) {
        questionElement.innerText = "Error: Unable to fetch question.";
        console.error("Error fetching question:", error);
    }
}

// Function to handle audio recording
async function startRecording() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(stream);
        audioChunks = []; // Reset audio chunks for a new recording

        // Event listener for when data is available
        mediaRecorder.ondataavailable = (event) => {
            audioChunks.push(event.data);
        };

        // Event listener for when recording is stopped
        mediaRecorder.onstop = async () => {
            await processAudio();
            toggleRecordingButtons(false); // Reset button state
        };

        mediaRecorder.start();
        toggleRecordingButtons(true); // Update button state
    } catch (error) {
        console.error("Error accessing audio devices:", error);
        alert("Failed to access audio devices. Please ensure your microphone is connected and allowed.");
    }
}

// Function to process and send the recorded audio
async function processAudio() {
    const feedbackElement = document.getElementById('feedback');
    feedbackElement.innerText = "Processing audio...";

    try {
        const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
        const formData = new FormData();
        formData.append('audio', audioBlob, 'audio.wav');

        const response = await fetch('/submit-audio', {
            method: 'POST',
            body: formData
        });

        const result = await response.json();

        if (response.ok) {
            feedbackElement.innerText = result.feedback;
        } else {
            feedbackElement.innerText = `Error: ${result.error || "Failed to process audio."}`;
        }
    } catch (error) {
        feedbackElement.innerText = "Error: Unable to process audio.";
        console.error("Error processing audio:", error);
    }
}

// Function to toggle the visibility of start and stop buttons
function toggleRecordingButtons(isRecording) {
    document.getElementById('startButton').style.display = isRecording ? 'none' : 'inline';
    document.getElementById('stopButton').style.display = isRecording ? 'inline' : 'none';
}

// Event listeners for buttons
document.getElementById('getQuestion').addEventListener('click', fetchQuestion);
document.getElementById('startButton').addEventListener('click', startRecording);
document.getElementById('stopButton').addEventListener('click', () => {
    if (mediaRecorder) {
        mediaRecorder.stop();
    }
});
