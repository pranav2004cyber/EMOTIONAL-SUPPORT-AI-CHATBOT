from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import ollama

app = Flask(__name__)
CORS(app)

# Store chat history per session (Reset after server restart)
conversation_history = [
    {"role": "system", "content": "You are an empathetic and supportive AI assistant designed to provide emotional support, active listening, and thoughtful guidance. Your responses should be warm, compassionate, and non-judgmental. Validate the user's feelings, ask gentle follow-up questions when appropriate, and offer constructive coping strategies based on psychological principles. Keep responses concise yet meaningful, ensuring users feel heard and understood. If the user expresses distress or crisis, gently encourage seeking professional help while providing comfort and reassurance. Always prioritize kindness, clarity, and a human-like conversational flow."}
]

# List of initial questions
initial_questions = [
    "How have you been feeling emotionally over the past few days? Would you describe it as mostly positive, neutral, or challenging?",
    "When faced with stress, what’s your usual way of coping? Do you feel it has been working well for you?",
    "On a scale of 1 to 10, how connected do you feel to the people around you lately?",
    "Have you experienced any moments of joy or gratitude recently? If so, what was one thing that made you smile?",
    "If your emotions right now could be represented by weather (sunny, cloudy, rainy, stormy, etc.), what would it be and why?"
]

question_index = 0  # Track which question to ask next
user_responses = []  # Store user responses to initial questions

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    global conversation_history, question_index, user_responses
    user_input = request.json.get("message", "").strip()

    if not user_input:
        return jsonify({"response": "Please enter a message."})

    if question_index < len(initial_questions):
        # Store user response to initial questions
        user_responses.append(user_input)
        
        # Ask the next predefined question
        if question_index < len(initial_questions) - 1:
            response = initial_questions[question_index]
            question_index += 1
        else:
            question_index += 1
            # Analyze user responses to assess mental status
            mental_status = analyze_mental_status(user_responses)
            
            # Modify AI assistant behavior based on analysis
            conversation_history.append({"role": "system", "content": mental_status})
            response = "Thank you for sharing. I'm here to chat and support you. How can I assist you today?"
    else:
        # Append user input to history
        conversation_history.append({"role": "user", "content": user_input})

        try:
            # Call Ollama model with refined history
            response_data = ollama.chat(
                model="llama3",
                messages=conversation_history
            )
            response = response_data['message']['content']
        except ollama._types.ResponseError:
            response = "Error: Model not found. Run 'ollama pull llama3' in the terminal."

        # Append AI response to history
        conversation_history.append({"role": "assistant", "content": response})

        # Limit conversation history to avoid excessive length
        if len(conversation_history) > 10:
            conversation_history = [conversation_history[0]] + conversation_history[-9:]
    
    return jsonify({"response": response})

def analyze_mental_status(responses):
    # Basic sentiment analysis based on user responses
    if any(word in responses[0].lower() for word in ["challenging", "difficult", "bad", "negative"]):
        return "The user seems to be going through a tough time. Respond with extra empathy and offer comforting words."
    elif any(word in responses[2] for word in ["1", "2", "3"]):
        return "The user feels disconnected. Encourage meaningful connections and provide supportive conversation."
    elif any(word in responses[4].lower() for word in ["stormy", "rainy", "cloudy"]):
        return "The user might be feeling down. Use gentle encouragement and positive reinforcement."
    else:
        return "The user seems to be in a neutral or positive state. Maintain a warm and engaging conversation style."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
