import streamlit as st
import speech_recognition as sr
from deep_translator import GoogleTranslator
from pydub import AudioSegment
import tempfile

# Language mapping: Full form ↔️ Language code
LANGUAGES = {
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
st.write("Upload an audio file and get transcription + translation to your language!")

# Dropdown with full language names
selected_lang_name = st.selectbox("Translate to", list(LANGUAGES.keys()), index=2)
lang_target = LANGUAGES[selected_lang_name]  # Convert to language code

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
            st.info("🔄 Transcribing...")
            try:
                text = recognizer.recognize_google(audio_data)
                st.success("✅ Transcription Complete!")
                st.markdown(f"**📝 Original Transcript (English):** {text}")

                translated = GoogleTranslator(source='auto', target=lang_target).translate(text)
                st.markdown(f"🌐 **Translated to {selected_lang_name}:** {translated}")

            except sr.UnknownValueError:
                st.error("❌ Could not understand the audio.")
            except sr.RequestError:
                st.error("⚠️ API unavailable or quota exceeded.")
