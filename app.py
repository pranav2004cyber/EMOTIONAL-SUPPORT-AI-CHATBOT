from flask import Flask, request, jsonify, session, redirect, url_for, render_template
from flask_bcrypt import Bcrypt
from flask_cors import CORS
import mysql.connector
import os
from flask_cors import CORS
import ollama
from functools import wraps

# Initialize Flask App
app = Flask(__name__) 
app.secret_key = 'your_secret_key'  # Required for session management
bcrypt = Bcrypt(app)
CORS(app)  # Allow cross-origin requests

# MySQL Database Configuration
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "1234",
    "database": "haven_db"
}

# Function to Connect to MySQL
def get_db_connection():
    return mysql.connector.connect(**db_config)

conversation_history = [
    {"role": "system", "content": "You are an empathetic and supportive AI assistant named HAVEN designed to provide emotional support, active listening, and thoughtful guidance. Your responses should be warm, compassionate, and non-judgmental. Validate the user's feelings, ask gentle follow-up questions when appropriate, and offer constructive coping strategies based on psychological principles. Keep responses concise yet meaningful, ensuring users feel heard and understood. If the user expresses distress or crisis, gently encourage seeking professional help while providing comfort and reassurance. Always prioritize kindness, clarity, and a human-like conversational flow. Also add emojis according to the conversation."}
]

initial_questions = [
    "How have you been feeling emotionally over the past few days?\n a) Mostly positive 😊\n b) Neutral 😐\n c) Challenging 😞\n d) Ups and downs 🎭",
    "When faced with stress, how do you usually cope?\n a) Talking to someone about it 🗣️\n b) Distracting myself with activities 🎮📚\n c) Keeping it to myself 🤐\n d) I’m not sure how to cope 😕",
    "On a scale of 1 to 10, how connected do you feel to the people around you lately?\n a) 8-10 (Very connected) ❤️\n b) 5-7 (Somewhat connected) 🙂\n c) 2-4 (A bit disconnected) 😔\n d) 1 (Completely isolated) 😞",
    "Have you experienced any moments of joy or gratitude recently?\n a) Yes, many! 🎉\n b) A few, but not much 🤷\n c) Not really, it’s been tough 😞\n d) I don’t remember 😕",
    "If your emotions right now could be represented by weather, what would it be?\n a) Sunny (Feeling great!) ☀️\n b) Partly cloudy (Doing okay) 🌤️\n c) Rainy (Feeling down) 🌧️\n d) Stormy (Overwhelmed) ⛈️"
]

valid_options = {"a", "b", "c", "d"}
question_index = 0
user_responses = []
first_message = True

@app.route("/")
def home():
    return render_template("login.html")

@app.route("/chat", methods=["POST"])
def chat():
    global conversation_history, question_index, user_responses, first_message
    
    user_input = request.json.get("message", "").strip().lower()
    
    if not user_input:
        return jsonify({"response": "Please enter a message."})

    # First message handling
    if first_message:
        first_message = False
        response = initial_questions[question_index]
        question_index += 1  # Move to next question
        return jsonify({"response": response})

    # Handling the questionnaire phase
    if question_index <= len(initial_questions):
        if user_input not in valid_options:
            return jsonify({"response": "Please enter a valid option (a, b, c, or d)."})

        user_responses.append(user_input)

        # If last question was just answered, perform analysis
        if question_index == len(initial_questions):
            mental_status = analyze_mental_status(user_responses)
            conversation_history.append({"role": "system", "content": mental_status})
            question_index += 1  # Move past questionnaire phase
            return jsonify({"response": "Thank you for sharing. I'm here to chat and support you. How can I assist you today?"})

        response = initial_questions[question_index]  # Ask next question
        question_index += 1  # Move to next question
        return jsonify({"response": response})

    # Normal chat after questionnaire is completed
    conversation_history.append({"role": "user", "content": user_input})

    try:
        response_data = ollama.chat(
            model="llama3",
            messages=conversation_history
        )
        response = response_data['message']['content']
    except ollama._types.ResponseError:
        response = "Error: Model not found. Run 'ollama pull llama3' in the terminal."

    conversation_history.append({"role": "assistant", "content": response})

    # Maintain chat history limit
    if len(conversation_history) > 10:
        conversation_history = [conversation_history[0]] + conversation_history[-9:]

    return jsonify({"response": response})

def analyze_mental_status(responses):
    if "c" in responses[0] or "d" in responses[0]:
        return "The user seems to be going through a tough time. Respond with extra empathy and offer comforting words."
    elif "c" in responses[1] or "d" in responses[1]:
        return "The user struggles with stress management. Respond accordingly so that the user feels less stressed."
    elif "d" in responses[2]:
        return "The user feels completely isolated. Encourage meaningful connections and provide supportive conversation."
    elif "c" in responses[3] or "d" in responses[3]:
        return "The user has been struggling to find joy or gratitude. Encourage small moments of positivity and mindfulness."
    elif "c" in responses[4] or "d" in responses[4]:
        return "The user might be feeling down. Use gentle encouragement and positive reinforcement."
    else:
        return "The user seems to be in a neutral or positive state. Maintain a warm and engaging conversation style."

@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"message": "Username and password are required!"}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "User registered successfully!"}), 201
    except mysql.connector.Error as err:
        return jsonify({"message": "Error: " + str(err)}), 500

# Route for Login
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"message": "Username and password are required!"}), 400

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user and bcrypt.check_password_hash(user['password'], password):
            session['username'] = username  # Set session variable
            return jsonify({"message": "Login successful!", "redirect": url_for('index')}), 200
        else:
            return jsonify({"message": "Invalid username or password!"}), 401
    except mysql.connector.Error as err:
        return jsonify({"message": "Error: " + str(err)}), 500

# Decorator to check if user is logged in
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('home'))
        return f(*args, **kwargs)
    return decorated_function

# Route for Index Page (After Login)
@app.route('/index')
@login_required
def index():
    return render_template('index.html')

# Route for Logout
@app.route('/logout')
def logout():
    session.pop('username', None)  # Clear the session
    return redirect(url_for('home'))  # Redirect to the home route, which renders login.html

if __name__ == '__main__':
    app.run(debug=True)