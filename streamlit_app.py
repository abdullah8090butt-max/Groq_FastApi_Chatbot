import streamlit as st
from groq import Groq
import os
import tempfile
from dotenv import load_dotenv


# ==========================================
# LOAD ENVIRONMENT
# ==========================================

load_dotenv()


# ==========================================
# PAGE SETTINGS
# ==========================================

st.set_page_config(
    page_title="AI Personal Assistant",
    page_icon="🤖",
    layout="centered"
)


# ==========================================
# GET API KEY
# ==========================================

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    try:
        api_key = st.secrets["GROQ_API_KEY"]
    except Exception:
        api_key = None


if not api_key:
    st.error("❌ GROQ_API_KEY is not configured.")
    st.stop()


# ==========================================
# GROQ CLIENT
# ==========================================

@st.cache_resource
def get_groq_client():
    return Groq(api_key=api_key)


client = get_groq_client()


# ==========================================
# TITLE
# ==========================================

st.title("🤖 AI Personal Assistant")

st.caption(
    "Ask questions using text or your voice."
)


# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.title("⚙️ Settings")

voice_output = st.sidebar.toggle(
    "🔊 Enable Voice Output",
    value=False
)

if voice_output:

    st.sidebar.warning(
        "🔊 Voice ON — limited TTS is being used."
    )

else:

    st.sidebar.success(
        "⚡ Fast Mode — Voice OFF."
    )


# ==========================================
# SESSION STATE
# ==========================================

if "messages" not in st.session_state:
    st.session_state.messages = []


if "voice_key" not in st.session_state:
    st.session_state.voice_key = 0


# ==========================================
# AI RESPONSE
# ==========================================

def get_ai_response(question):

    response = client.chat.completions.create(

        model="openai/gpt-oss-20b",

        messages=[
            {
                "role": "user",
                "content": question
            }
        ],

        max_tokens=500
    )

    return response.choices[0].message.content


# ==========================================
# SPEECH TO TEXT
# ==========================================

def speech_to_text(audio_file):

    transcription = client.audio.transcriptions.create(

        file=(
            audio_file.name,
            audio_file.getvalue()
        ),

        model="whisper-large-v3-turbo",

        response_format="json"
    )

    return transcription.text


# ==========================================
# TEXT TO SPEECH
# ==========================================

def text_to_speech(text):

    text = text.strip()

    if not text:
        return None


    # Limit TTS usage

    if len(text) > 200:

        text = text[:200]

        last_space = text.rfind(" ")

        if last_space > 50:
            text = text[:last_space]

        text += "..."


    # Generate speech

    speech_response = client.audio.speech.create(

        model="canopylabs/orpheus-v1-english",

        voice="troy",

        input=text,

        response_format="wav"
    )


    # Temporary file

    temp_file = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".wav"
    )

    temp_file.close()


    # Save speech

    speech_response.write_to_file(
        temp_file.name
    )


    # Read audio

    with open(
        temp_file.name,
        "rb"
    ) as audio:

        audio_bytes = audio.read()


    # Delete temporary file

    os.remove(
        temp_file.name
    )


    return audio_bytes


# ==========================================
# MAIN CHAT FRAGMENT
# ==========================================

@st.fragment
def chat_area():

    # ======================================
    # CHAT DISPLAY
    # ======================================

    st.subheader("💬 Conversation")


    chat_container = st.container(
        height=500,
        border=True
    )


    with chat_container:

        if not st.session_state.messages:

            st.info(
                "👋 Hello! Ask me anything."
            )

        else:

            for message in st.session_state.messages:

                with st.chat_message(
                    message["role"]
                ):

                    st.markdown(
                        message["content"]
                    )


                    if (
                        message["role"] == "assistant"
                        and message.get("audio")
                    ):

                        st.audio(
                            message["audio"],
                            format="audio/wav"
                        )


    # ======================================
    # VOICE INPUT
    # ======================================

    st.subheader("🎤 Voice Input")

    st.write(
        "Speak your question. After the answer, "
        "you can record another question."
    )


    # IMPORTANT:
    # A new key is created after every recording.
    # This allows the microphone to record again.

    audio_input = st.audio_input(
        "🎤 Record your question",
        key=f"voice_input_{st.session_state.voice_key}"
    )


    # ======================================
    # PROCESS VOICE
    # ======================================

    if audio_input is not None:

        try:

            # ----------------------------------
            # SPEECH TO TEXT
            # ----------------------------------

            with st.spinner(
                "🎤 Converting voice to text..."
            ):

                question = speech_to_text(
                    audio_input
                )


            if not question.strip():

                st.warning(
                    "⚠️ I could not understand your voice. "
                    "Please try again."
                )

                return


            # ----------------------------------
            # SAVE USER QUESTION
            # ----------------------------------

            st.session_state.messages.append(
                {
                    "role": "user",
                    "content": question
                }
            )


            # ----------------------------------
            # AI RESPONSE
            # ----------------------------------

            with st.spinner(
                "🤖 Thinking..."
            ):

                answer = get_ai_response(
                    question
                )


            # ----------------------------------
            # CREATE MESSAGE
            # ----------------------------------

            message_data = {
                "role": "assistant",
                "content": answer
            }


            # ----------------------------------
            # TTS ONLY WHEN ENABLED
            # ----------------------------------

            if voice_output:

                try:

                    with st.spinner(
                        "🔊 Generating voice..."
                    ):

                        audio = text_to_speech(
                            answer
                        )


                    if audio:

                        message_data["audio"] = audio


                except Exception as e:

                    error_message = str(e)

                    if "429" in error_message:

                        st.warning(
                            "⚠️ TTS limit reached. "
                            "The text answer is still available."
                        )

                    else:

                        st.warning(
                            "⚠️ Voice generation failed."
                        )


            # ----------------------------------
            # SAVE AI ANSWER
            # ----------------------------------

            st.session_state.messages.append(
                message_data
            )


            # ----------------------------------
            # CREATE NEW MICROPHONE
            # ----------------------------------

            st.session_state.voice_key += 1


            # ----------------------------------
            # REFRESH ONLY THIS FRAGMENT
            # ----------------------------------

            st.rerun(scope="fragment")


        except Exception as e:

            st.error(
                "❌ Voice error: " + str(e)
            )


    # ======================================
    # TEXT CHAT
    # ======================================

    question = st.chat_input(
        "Ask me anything..."
    )


    if question:

        # ----------------------------------
        # SAVE USER QUESTION
        # ----------------------------------

        st.session_state.messages.append(
            {
                "role": "user",
                "content": question
            }
        )


        try:

            # ----------------------------------
            # AI RESPONSE
            # ----------------------------------

            with st.spinner(
                "🤖 Thinking..."
            ):

                answer = get_ai_response(
                    question
                )


            # ----------------------------------
            # CREATE MESSAGE
            # ----------------------------------

            message_data = {
                "role": "assistant",
                "content": answer
            }


            # ----------------------------------
            # TTS
            # ----------------------------------

            if voice_output:

                try:

                    with st.spinner(
                        "🔊 Generating voice..."
                    ):

                        audio = text_to_speech(
                            answer
                        )


                    if audio:

                        message_data["audio"] = audio


                except Exception as e:

                    error_message = str(e)

                    if "429" in error_message:

                        st.warning(
                            "⚠️ TTS limit reached. "
                            "The text answer is still available."
                        )

                    else:

                        st.warning(
                            "⚠️ Voice generation failed."
                        )


            # ----------------------------------
            # SAVE ANSWER
            # ----------------------------------

            st.session_state.messages.append(
                message_data
            )


            # ----------------------------------
            # REFRESH ONLY CHAT FRAGMENT
            # ----------------------------------

            st.rerun(scope="fragment")


        except Exception as e:

            st.error(
                "❌ Error: " + str(e)
            )


# ==========================================
# RUN CHAT
# ==========================================

chat_area()


# ==========================================
# CLEAR CHAT
# ==========================================

st.divider()


if st.button(
    "🧹 Clear Chat",
    use_container_width=True
):

    st.session_state.messages = []

    st.session_state.voice_key = 0

    st.rerun()