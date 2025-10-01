
The AI Accent Coach is an interactive web application designed to help non-native English speakers improve their pronunciation. It provides real-time feedback by recording a user's voice, analyzing the pronunciation against a phonetic model, and delivering an objective score.

Features
Interactive UI: A modern, dark-themed interface with real-time audio visualization.

Word Selection: Practice from a predefined list of challenging English words.

Accent Listening: Listen to the correct pronunciation in American, British, or Australian accents using native browser text-to-speech.

AI-Powered Analysis: Records user audio and sends it to a Python backend for analysis.

Phonetic Scoring: The core of the project, this feature compares the phonetic sounds of the user's speech to the target word's sounds, providing a score based on pronunciation accuracy.

Detailed Feedback: Displays the final score, a text comparison, and a phonetic guide for the target word.

Technology Stack
Frontend:

HTML5

Tailwind CSS for styling

JavaScript (for audio recording, UI interaction, and API communication)

Backend:

Python 3

Flask (as the web server)

SpeechRecognition (using the Google Speech-to-Text API)

pydub (for audio format conversion)

pronouncing & difflib (for phonetic analysis and scoring)

Core Dependency:

FFmpeg: A powerful multimedia framework used by pydub for audio conversion.

System Requirements
Before you begin, ensure you have the following installed on your system:

Python 3.8+ and pip.

FFmpeg: This is a crucial dependency for audio processing. If you don't have it, please follow an online guide to install it for your operating system (Windows, macOS, or Linux).

Setup Instructions
Download the Project Files:
Make sure all project files (index.html, app.py, requirements.txt) are in a single folder on your computer.

Install Python Libraries:
Open your terminal or command prompt, navigate to your project folder, and run the following command to install all the necessary Python packages:

pip install -r requirements.txt

Running the Application (Two-Terminal Setup)
This project requires two separate servers to run simultaneously: one for the Python backend and one to serve the HTML frontend.

1. Start the Backend Server (Terminal 1)

Open your first terminal.

Navigate to the project directory.

Run the Flask server:

python app.py

You should see output indicating the server is running on http://127.0.0.1:5000. Keep this terminal open.

2. Start the Frontend Server (Terminal 2)

Open a second, new terminal window.

Navigate to the same project directory.

Run Python's built-in HTTP server:

python -m http.server 8000

You should see output like Serving HTTP on ... port 8000. Keep this terminal open as well.

How to Use
With both servers running, open your web browser.

Go to the following address:

http://localhost:8000

Select a word and an accent, click "Listen" to hear it, and then "Record" to try it yourself!
