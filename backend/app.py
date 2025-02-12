import requests
import os
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

# Initialize Flask app
app = Flask(__name__)
socketio = SocketIO(app)

# Get Hugging Face API Key from environment variable
HF_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

# Ensure the API key is set
if not HF_API_KEY:
    print("⚠️ Error: HUGGINGFACE_API_KEY is not set! Set it using 'export HUGGINGFACE_API_KEY=your-key' or Windows env variables.")
    exit(1)  # Stop execution if API key is missing

# Function to get AI response from Hugging Face API
def get_ai_response(user_input):
    url = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"  # Free chatbot model
    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    payload = {"inputs": user_input}

    try:
        response = requests.post(url, headers=headers, json=payload)

        # Debugging - Print API response status
        print(f"API Response Status: {response.status_code}")
        print(f"API Response Text: {response.text}")

        if response.status_code == 200:
            return response.json()[0].get("generated_text", "I don't understand that.")
        elif response.status_code == 503:
            return "Model is currently loading. Please try again in a few seconds."
        elif response.status_code == 401:
            return "Invalid API Key. Check your Hugging Face API key."
        else:
            return f"API Error: {response.json()}"
    except Exception as e:
        print(f"⚠️ Error: {e}")
        return "I'm not sure how to respond to that."

# Handle messages from frontend
@socketio.on("message")
def handle_message(data):
    user_message = data["text"]
    bot_reply = get_ai_response(user_message)
    emit("response", {"text": bot_reply}, broadcast=True)

# Flask route for frontend
@app.route("/")
def index():
    return render_template("index.html")

# Run the Flask app
if __name__ == "__main__":
    socketio.run(app, debug=True)





