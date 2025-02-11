# HAVEN.AI

## Overview
HAVEN.AI is an emotional support chatbot built using Streamlit and the Ollama API. It provides conversational support, positive affirmations, and guided meditation scripts to help users manage stress and emotional well-being.

## Features
- **Conversational AI**: Users can chat with the AI, and their conversation history is maintained within the session.
- **Background Customization**: A background image (`background.png`) is loaded and applied to the interface.
- **Positive Affirmations**: Generates motivational messages for users.
- **Guided Meditation**: Provides a short guided meditation script to help users relax.

## Requirements
Ensure you have the following installed:
- Python 3.8+
- Streamlit (`pip install streamlit`)
- Ollama (`pip install ollama`)
- Base64 module (built-in with Python)

## Installation & Setup
1. Clone the repository or download the script.
2. Install the required dependencies:
   ```sh
   pip install streamlit ollama
   ```
3. Make sure you have the `background.png` file in the same directory.
4. Pull the required AI model by running:
   ```sh
   ollama pull llama3
   ```
5. Run the Streamlit app:
   ```sh
   streamlit run app.py
   ```

## Usage
- Enter your message in the chat input field to start a conversation.
- Click **"Give me a Positive Affirmation"** to receive an uplifting message.
- Click **"Give me a Guided Meditation"** for a 5-minute meditation script.

## Troubleshooting
- If the AI model is not found, ensure you have run `ollama pull llama3`.
- If the background image does not load, verify `background.png` exists in the correct directory.

## License
This project is open-source. Feel free to modify and improve it!

