from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Gemini API base URL and API key
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent"
API_KEY = "AIzaSyC1d3uER9eKSxpSmYM-eE0__yj1byMJrDA"  # Replace with your actual API key

# Route to serve the webpage
@app.route('/')
def index():
    return render_template('index.html')

# Function to get a question from Gemini API based on the domain
def get_question_from_gemini(domain):
    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": f"Generate an insightful interview question for a {domain} role."
                    }
                ]
            }
        ]
    }
    
    response = requests.post(f"{GEMINI_API_URL}?key={API_KEY}", json=payload)

    if response.status_code == 200:
        questions = response.json().get('candidates', [])
        if questions:
            return questions[0]['content']['parts'][0]['text']  # Return the first question
        return "No questions generated."
    else:
        try:
            error_response = response.json()
            print("API Error Response:", error_response)
            return f"Error: {error_response.get('message', 'Failed to generate question.')}"
        except ValueError:
            print("Received non-JSON response:", response.text)
            return "Error: Received non-JSON response."

# API route to get a question based on the selected field
@app.route('/get-question/<domain>', methods=['GET'])
def get_question(domain):
    question = get_question_from_gemini(domain)
    return jsonify({"question": question})

# Function to analyze audio and get feedback
def analyze_audio_with_gemini(audio_file):
    files = {
        'file': audio_file
    }

    response = requests.post(f"{GEMINI_API_URL}/analyze-audio?key={API_KEY}", files=files)

    if response.status_code == 200:
        feedback = response.json().get('feedback', "Error: No feedback available.")
        return feedback
    else:
        try:
            error_response = response.json()
            print("API Error Response:", error_response)
            return f"Error: {error_response.get('message', 'Failed to process audio.')}"
        except ValueError:
            print("Received non-JSON response:", response.text)
            return "Error: Received non-JSON response."

# API route to handle audio submission and feedback generation
@app.route('/submit-audio', methods=['POST'])
def submit_audio():
    if 'audio' not in request.files:
        return jsonify({"error": "No audio file uploaded"}), 400
    
    audio_file = request.files['audio']
    
    print("Uploaded audio file name:", audio_file.filename)
    print("Uploaded audio file type:", audio_file.content_type)

    feedback = analyze_audio_with_gemini(audio_file)

    return jsonify({"feedback": feedback})

if __name__ == '__main__':
    app.run(debug=True)


# from flask import Flask, render_template, request, jsonify
# import requests

# app = Flask(__name__)

# # Gemini API base URL and API key
# GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent"
# API_KEY = "AIzaSyAv3Fy4YS9-71tXusIO2wVvK1YUzUY24Cs"

# # Route to serve the webpage
# @app.route('/')
# def index():
#     return render_template('index.html')

# # Function to get questions from Gemini API based on the domain
# def get_questions_from_gemini(domain):
#     payload = {
#         "contents": [
#             {
#                 "parts": [
#                     {
#                         "text": f"Generate 5 insightful interview questions for a {domain} role."
#                     }
#                 ]
#             }
#         ]
#     }
    
#     response = requests.post(f"{GEMINI_API_URL}?key={API_KEY}", json=payload)

#     if response.status_code == 200:
#         questions = response.json().get('candidates', [])
#         return [question['content']['parts'][0]['text'] for question in questions[:5]]
#     else:
#         print("API Error Response:", response.json())  # Log API error response
#         return ["Error: Could not generate questions."]

# # API route to get questions based on the selected field
# @app.route('/get-questions/<domain>', methods=['GET'])
# def get_questions(domain):
#     questions = get_questions_from_gemini(domain)
#     return jsonify({"questions": questions})

# # Function to send audio to Gemini API for analysis
# def analyze_audio_with_gemini(audio_file):
#     # Send audio to Gemini API
#     files = {
#         'file': audio_file  # Ensure this key matches the API's expectations
#     }

#     response = requests.post(f"{GEMINI_API_URL}/analyze-audio?key={API_KEY}", files=files)

#     # Return feedback from Gemini API in JSON format
#     if response.status_code == 200:
#         try:
#             feedback = response.json().get('feedback', "Error: No feedback available.")
#             return feedback
#         except ValueError:
#             print("Received non-JSON response:", response.text)  # Log non-JSON responses
#             return "Error: Received non-JSON response."
#     else:
#         try:
#             error_response = response.json()
#             print("API Error Response:", error_response)  # Log API error response
#             return f"Error: {error_response.get('message', 'Failed to process audio.')}"
#         except ValueError:
#             print("Received non-JSON error response:", response.text)  # Log non-JSON error responses
#             return "Error: Received non-JSON error response."

# # API route to handle audio submission and feedback generation
# @app.route('/submit-audio', methods=['POST'])
# def submit_audio():
#     if 'audio' not in request.files:
#         return jsonify({"error": "No audio file uploaded"}), 400
    
#     audio_file = request.files['audio']
    
#     # Log audio file details
#     print("Uploaded audio file name:", audio_file.filename)
#     print("Uploaded audio file type:", audio_file.content_type)

#     # Send the audio file to Gemini API for analysis
#     feedback = analyze_audio_with_gemini(audio_file)

#     return jsonify({"feedback": feedback})

# if __name__ == '__main__':
#     app.run(debug=True)

