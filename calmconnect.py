import streamlit as st
import ollama
import base64
import os

st.set_page_config(page_title="HAVEN.AI")

# Function to load background image
def get_base64(background):
    try:
        with open(background, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except FileNotFoundError:
        return None  # Return None if the file is missing

background_image = get_base64("background.png")

if background_image:
    st.markdown(f"""
        <style>
            .main{{
                background-image: url("data:image/png;base64,{background_image}");
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
            }}
        </style>
    """, unsafe_allow_html=True)

# Initialize conversation history
st.session_state.setdefault('conversation_history', [])

# Function to generate response
def generate_response(user_input):
    st.session_state['conversation_history'].append({"role": "user", "content": user_input})

    try:
        response = ollama.chat(model="llama3", messages=st.session_state['conversation_history'])
        ai_response = response['message']['content']
    except ollama._types.ResponseError:
        ai_response = "Error: The model is not found. Run 'ollama pull llama3' in the terminal."

    st.session_state['conversation_history'].append({"role": "assistant", "content": ai_response})
    return ai_response

# Function to generate positive affirmations
def generate_affirmation():
    prompt = "Provide a positive affirmation to encourage someone who is feeling stressed or overwhelmed."
    response = ollama.chat(model="llama3", messages=[{"role": "user", "content": prompt}])
    return response['message']['content']

# Function to generate a guided meditation script
def generate_meditation_guide():
    prompt = "Provide a 5-minute guided meditation script to help someone relax and reduce stress."
    response = ollama.chat(model="llama3", messages=[{"role": "user", "content": prompt}])
    return response['message']['content']

# App UI
st.title("EMOTIONAL SUPPORT CHATBOT")

# Display conversation history
for msg in st.session_state['conversation_history']:
    role = "You" if msg['role'] == "user" else "AI"
    st.markdown(f"**{role}:** {msg['content']}")

# User input
user_message = st.text_input("How can I help you today?")

if user_message:
    with st.spinner("Thinking..."):
        ai_response = generate_response(user_message)
        st.markdown(f"**AI:** {ai_response}")

# Columns for extra features
col1, col2 = st.columns(2)

with col1:
    if st.button("Give me a Positive Affirmation"):
        affirmation = generate_affirmation()
        st.markdown(f"**Affirmation:** {affirmation}")

with col2:
    if st.button("Give me a Guided Meditation"):
        meditation_guide = generate_meditation_guide()
        st.markdown(f"**Guided Meditation:** {meditation_guide}")
