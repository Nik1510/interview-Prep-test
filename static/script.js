async function fetchJSON(url) {
    try {
        const response = await fetch(url);

        // Check if the response is JSON
        const contentType = response.headers.get("content-type");
        if (!contentType || !contentType.includes("application/json")) {
            throw new Error("Received non-JSON response.");
        }

        return await response.json(); // Parse the JSON response
    } catch (error) {
        console.error("Error fetching JSON data:", error);
        throw error; // Re-throw the error for handling outside
    }
}

document.getElementById('getQuestion').onclick = async () => {
    const domain = document.getElementById('domain').value;
    try {
        const result = await fetchJSON(`/get-question/${domain}`);
        const cleanedQuestion = result.question.replace(/[#*]/g, '').trim(); // Clean up the question
        document.getElementById('question').innerText = cleanedQuestion;
    } catch (error) {
        document.getElementById('question').innerText = "Error fetching question.";
    }
};

document.getElementById('startButton').onclick = async () => {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(stream);

        mediaRecorder.ondataavailable = (event) => {
            audioChunks.push(event.data);
        };

        mediaRecorder.onstop = async () => {
            const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
            const formData = new FormData();
            formData.append('audio', audioBlob, 'audio.wav');

            try {
                const response = await fetch('/submit-audio', {
                    method: 'POST',
                    body: formData
                });

                const contentType = response.headers.get("content-type");
                if (!contentType || !contentType.includes("application/json")) {
                    throw new Error("Received non-JSON response.");
                }

                const result = await response.json();
                document.getElementById('feedback').innerText = result.feedback || "No feedback available.";
            } catch (error) {
                console.error("Error submitting audio:", error);
                document.getElementById('feedback').innerText = "Error submitting audio.";
            }
        };

        mediaRecorder.start();
        document.getElementById('stopButton').style.display = 'block';
        document.getElementById('startButton').style.display = 'none';
    } catch (error) {
        console.error('Error accessing audio devices:', error);
    }
};

document.getElementById('stopButton').onclick = () => {
    mediaRecorder.stop();
    audioChunks = []; // Reset audio chunks for the next recording
    document.getElementById('stopButton').style.display = 'none';
    document.getElementById('startButton').style.display = 'block';
};
