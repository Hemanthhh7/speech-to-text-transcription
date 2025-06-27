import streamlit as st
import speech_recognition as sr
from deep_translator import GoogleTranslator
from pydub import AudioSegment
import tempfile
from moviepy.editor import VideoFileClip
import os

# Language map for display
LANG_DISPLAY = {
    "en": "English",
    "hi": "Hindi",
    "te": "Telugu",
    "ta": "Tamil",
    "bn": "Bengali",
    "ml": "Malayalam",
    "gu": "Gujarati",
    "ur": "Urdu"
}

st.set_page_config(page_title="🗣️ Video & Audio Speech Translator")
st.title("🗣️ Multilingual Speech Transcription & Translation")

st.write("Upload an audio or video file. Get transcription in English and translation in your selected language.")

# Select language
lang_target = st.selectbox("Translate to", list(LANG_DISPLAY.keys()), index=0,
                           format_func=lambda x: LANG_DISPLAY[x])

# Upload video/audio
uploaded_file = st.file_uploader("Upload Audio/Video file (MP3/WAV/FLAC/MP4/MKV)", type=["mp3", "wav", "flac", "mp4", "mkv"])

if uploaded_file:
    st.audio(uploaded_file, format="audio/mp3")
    st.info("📥 Processing...")

    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_input:
        tmp_input.write(uploaded_file.read())
        tmp_input.flush()

        # Extract audio if video
        if uploaded_file.name.endswith((".mp4", ".mkv")):
            st.info("🎞️ Extracting audio from video...")
            video = VideoFileClip(tmp_input.name)
            audio_path = tmp_input.name + ".wav"
            video.audio.write_audiofile(audio_path, verbose=False, logger=None)
        else:
            audio_path = tmp_input.name

        # Convert audio to WAV if not already
        if not audio_path.endswith(".wav"):
            audio = AudioSegment.from_file(audio_path)
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_wav:
                audio.export(tmp_wav.name, format="wav")
                audio_path = tmp_wav.name

        # Transcribe
        recognizer = sr.Recognizer()
        with sr.AudioFile(audio_path) as source:
            audio_data = recognizer.record(source)
            st.info("🧠 Transcribing with Google Speech API...")
            try:
                transcript = recognizer.recognize_google(audio_data)
                st.success("✅ Transcription Complete")
                st.markdown(f"### 📝 English Transcript:\n{transcript}")

                # Translate
                translated = GoogleTranslator(source='auto', target=lang_target).translate(transcript)
                st.markdown(f"### 🌍 Translated to {LANG_DISPLAY[lang_target]}:\n{translated}")
            except sr.UnknownValueError:
                st.error("❌ Could not understand the audio.")
            except sr.RequestError:
                st.error("⚠️ API unavailable or quota exceeded.")

