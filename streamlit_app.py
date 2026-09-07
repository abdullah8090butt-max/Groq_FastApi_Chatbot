import streamlit as st
import requests

# -----------------------------
# Page configuration
# -----------------------------
st.set_page_config(
    page_title="AI Chatbot",
    page_icon="🤖",
    layout="centered"
)

# -----------------------------
# Title
# -----------------------------
st.title("🤖 AI Chatbot")
st.caption("Powered by FastAPI + Groq")

# -----------------------------
# FastAPI URL
# -----------------------------
API_URL = "http://127.0.0.1:8000/predict"

# -----------------------------
# Chat history
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -----------------------------
# Display previous messages
# -----------------------------
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -----------------------------
# Chat input
# -----------------------------
question = st.chat_input("Ask me anything...")

if question:

    # Show user message
    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    with st.chat_message("user"):
        st.markdown(question)

    # Send question to FastAPI
    try:
        response = requests.post(
            API_URL,
            json={
                "question": question
            },
            timeout=60
        )

        # Check response
        if response.status_code == 200:

            data = response.json()
            answer = data["answer"]

            # Show AI response
            with st.chat_message("assistant"):
                st.markdown(answer)

            # Save AI response
            st.session_state.messages.append({
                "role": "assistant",
                "content": answer
            })

        else:

            st.error(
                f"API Error: {response.status_code}\n\n"
                f"{response.text}"
            )

    except requests.exceptions.ConnectionError:

        st.error(
            "❌ Cannot connect to FastAPI.\n\n"
            "Make sure your FastAPI server is running."
        )

    except requests.exceptions.Timeout:

        st.error(
            "⏱️ The request took too long. "
            "Please try again."
        )

    except Exception as e:

        st.error(f"Unexpected error: {e}")


# -----------------------------
# Clear chat button
# -----------------------------
if st.session_state.messages:

    if st.button("🗑️ Clear Chat"):

        st.session_state.messages = []

        st.rerun()