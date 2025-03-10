# Haven AI - Emotional Support Chatbot

Haven AI is an empathetic and supportive AI chatbot designed to provide emotional support, active listening, and thoughtful guidance. It helps users manage stress, anxiety, and mental well-being through AI-powered conversations, guided breathing exercises, and therapeutic music.

## Features
- **Emotional Support Chat**: Engage in supportive and non-judgmental conversations with Haven AI.
- **Guided Breathing Exercises**: Reduce stress and anxiety with interactive breathing exercises.
- **Therapeutic Music**: Listen to calming sounds to promote relaxation and mental well-being.

## Technologies Used
- **Backend**: Flask (Python), Ollama AI model (Llama3)
- **Frontend**: HTML, Tailwind CSS, JavaScript
- **API**: Flask REST API for chatbot communication

## Installation & Setup
### Prerequisites
Ensure you have the following installed:
- Python 3.8+
- Flask
- Flask-CORS
- Ollama

### Steps
1. Clone the repository:
   ```sh
   git clone https://github.com/pranav2004cyber/EMOTIONAL-SUPPORT-AI-CHATBOT.git
   cd haven-ai
   ```
2. Install dependencies:
   ```sh
   pip install flask flask-cors
   ```
3. Start the chatbot server:
   ```sh
   python app.py
   ```
4. Open `index.html` in a browser to interact with Haven AI.

## Usage
1. Open Haven AI in your browser.
2. Start chatting with the AI for emotional support.
3. Access guided breathing exercises for relaxation.
4. Listen to therapeutic music to enhance well-being.

## API Endpoints
- `GET /` - Loads the main page
- `POST /chat` - Sends user messages to Haven AI and receives responses

## Notes
- Haven AI maintains chat history per session.
- If the AI model is missing, run:
  ```sh
  ollama pull llama3
  ```
