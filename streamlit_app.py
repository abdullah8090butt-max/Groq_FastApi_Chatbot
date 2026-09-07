import streamlit as st
from groq import Groq
import os
from dotenv import load_dotenv

# Load .env for local use
load_dotenv()

# Page settings
st.set_page_config(
    page_title="AI Chatbot",
    page_icon="🤖"
)

# Get Groq API key
api_key = os.getenv("GROQ_API_KEY")

# Get Streamlit Cloud secret if .env is not available
if api_key is None:
    try:
        api_key = st.secrets["GROQ_API_KEY"]
    except Exception:
        api_key = None

# Check API key
if api_key is None:
    st.error("GROQ_API_KEY is not configured.")
    st.stop()

# Create Groq client
client = Groq(api_key=api_key)

# App title
st.title("🤖 AI Chatbot")
st.write("Powered by Groq + Streamlit")

# Create chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Chat input
question = st.chat_input("Ask me anything...")

if question:

    # Add user message
    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    # Display user message
    with st.chat_message("user"):
        st.write(question)

    try:

        # Generate AI response
        with st.spinner("Thinking..."):

            response = client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=[
                    {
                        "role": "user",
                        "content": question
                    }
                ]
            )

        # Get answer
        answer = response.choices[0].message.content

        # Display AI answer
        with st.chat_message("assistant"):
            st.write(answer)

        # Save AI answer
        st.session_state.messages.append({
            "role": "assistant",
            "content": answer
        })

    except Exception as e:
        st.error("Error: " + str(e))

# Clear chat button
if st.button("Clear Chat"):
    st.session_state.messages = []
    st.rerun()