import streamlit as st
import openai
import pyttsx3
import threading
from PIL import Image
import speech_recognition as sr

# Set OpenAI API credentials
api_key = "your_api_key"
openai.api_key = api_key

# Initialize recognizer
r = sr.Recognizer()

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty("rate", 150)

# Set Streamlit theme to Poe
st.set_page_config(
    page_title="Omega AI",
    page_icon=":book:",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Set logo and title
image = Image.open("logo.png")
st.sidebar.image(image, use_column_width=True)

# Streamlit UI layout
col1, col2 = st.columns([1, 3])
with col1:
    st.sidebar.write("")  # Set spacing between logo and microphone button

with col2:
    st.sidebar.text("Please enter a keyword")
    search_input = st.sidebar.text_input("")

# Function to generate AI response
def generate_response(query):
    response = openai.Completion.create(
        engine="davinci",
        prompt=query,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.7
    )
    return response.choices[0].text.strip()

# Function to speak text
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to recognize user's speech
def recognize_speech():
    with sr.Microphone() as source:
        st.sidebar.write("Start listening...")
        audio = r.listen(source)

    try:
        st.sidebar.write("Recognizing text...")
        query = r.recognize_google(audio)
        st.sidebar.write(f"User said: {query}")
        return query
    except sr.UnknownValueError:
        st.sidebar.write("Sorry, I couldn't recognize the speech.")
        return ""
    except sr.RequestError:
        st.sidebar.write("Sorry, there was an error processing the speech request.")
        return ""

# Function to read AI response
def read_response(response):
    st.write(response)
    speak_thread = threading.Thread(target=speak, args=(response,))
    speak_thread.start()  # Read AI response

# Search for information based on the entered keyword
if st.sidebar.button("Search"):
    if search_input:
        query = search_input
    else:
        query = recognize_speech()

    try:
        if query:
            ai_response = generate_response(query)
            read_response(ai_response)
    except Exception as e:
        st.write("An error occurred:", str(e))
        threading.Thread(target=speak, args=("Sorry, an error occurred.",)).start()