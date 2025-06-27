import streamlit as st
import speech_recognition as sr
from deep_translator import GoogleTranslator
from pydub import AudioSegment
import tempfile

# Language display names mapped to codes
LANGUAGES = {
    "Auto Detect": "auto",
    "English": "en",
    "Hindi": "hi",
    "Telugu": "te",
    "Tamil": "ta",
    "Bengali": "bn",
    "Malayalam": "ml",
    "Gujarati": "gu",
    "Urdu": "ur"
}

st.set_page_config(page_title="🗣️ Multilingual Transcription & Translation")
st.title("🗣️ Multilingual Speech Transcription & Translation")
st.write("Upload audio, select source/target languages, and get transcription + translation!")

# Language selectors
from_lang_name = st.selectbox("🎙️ From Language", list(LANGUAGES.keys()), index=0)  # Default: Auto
to_lang_name = st.selectbox("🌐 To Language", list(LANGUAGES.keys()), index=1)       # Default: English

from_lang = LANGUAGES[from_lang_name]
to_lang = LANGUAGES[to_lang_name]

uploaded_audio = st.file_uploader("Upload Audio (WAV/MP3/FLAC)", type=["wav", "mp3", "flac"])
if uploaded_audio:
    st.audio(uploaded_audio)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        if uploaded_audio.name.endswith(".mp3"):
            sound = AudioSegment.from_mp3(uploaded_audio)
        elif uploaded_audio.name.endswith(".flac"):
            sound = AudioSegment.from_file(uploaded_audio, format="flac")
        else:
            sound = AudioSegment.from_file(uploaded_audio)
        sound.export(tmp.name, format="wav")

        recognizer = sr.Recognizer()
        with sr.AudioFile(tmp.name) as source:
            audio_data = recognizer.record(source)
            st.info("🔄 Transcribing... (via Google Speech Recognition)")
            try:
                text = recognizer.recognize_google(audio_data, language=from_lang if from_lang != "auto" else "en-IN")
                st.success("✅ Transcription Complete!")
                st.markdown(f"**📝 Transcript:** {text}")

                translated = GoogleTranslator(source=from_lang, target=to_lang).translate(text)
                st.markdown(f"🌐 **Translated to {to_lang_name}:** {translated}")

            except sr.UnknownValueError:
                st.error("❌ Could not understand the audio.")
            except sr.RequestError:
                st.error("⚠️ API unavailable or quota exceeded.")
