import streamlit as st
import speech_recognition as sr
from deep_translator import GoogleTranslator
from pydub import AudioSegment
import tempfile

st.set_page_config(page_title="🗣️ Multilingual Transcription & Translation")
st.title("🗣️ Multilingual Speech Transcription & Translation")
st.write("Upload an audio file and get transcription + translation to your language!")

lang_target = st.selectbox("Translate to", ["en", "hi", "te", "ta", "bn", "ml", "gu", "ur"], index=2)

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
                st.markdown(f"🌐 **Translated to {lang_target.upper()}:** {translated}")

            except sr.UnknownValueError:
                st.error("❌ Could not understand the audio.")
            except sr.RequestError:
                st.error("⚠️ API unavailable or quota exceeded.")
